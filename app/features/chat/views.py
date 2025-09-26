from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app.features.ai.ai_logic import get_recipe_response

from .models import Ai_model_logs, ChatMessage, ChatSession
from .serializers import (AiModelLogsSerializer, ChatMessageSerializer,
                          ChatSessionSerializer)
from app.accounts.models import UserProfile

@api_view(["GET"])
def list_chats(request):
    """Return chat sessions with last message preview"""
    user = request.user
    chats = ChatSession.objects.filter(user=user).order_by("-updated_at")
    serializer = ChatSessionSerializer(chats, many=True)
    return Response(serializer.data, status=200)



@api_view(["POST"])
def send_message(request):
    user = request.user
    profile = user.profile
    message = request.data.get("message")
    chat_id = request.data.get("chat_id")
    title = request.data.get("title", "New Chat")
    if profile.recipe_generate > 2 and profile.is_subs is False :
        return Response({"error":"You have already generated your free 3 recipe. Please upgrade your plan","error_type":"plan_update_message"})
    if not message:
        return Response({"error": "Message cannot be empty"}, status=400)

    # --- Get or create chat ---
    if chat_id:
        try:
            chat = ChatSession.objects.get(id=chat_id, user=user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat not found"}, status=404)
    else:
        chat = ChatSession.objects.create(user=user, title=title)

    # --- Build conversation history ---
    history = []
    for msg in chat.messages.all().order_by("created_at"):
        if msg.content:
            history.append({"sender": msg.sender, "content": msg.content})
        elif msg.extra_data:
            history.append({"sender": msg.sender, "content": str(msg.extra_data)})
    history.append({"sender": "user", "content": message})

    # --- Call AI ---
    result = get_recipe_response(user_input=message, conversation_history=history)

    # --- Save user message ---
    ChatMessage.objects.create(
        chat=chat,
        sender="user",
        message_type="conversation",
        content=message
    )

    # --- Save assistant message depending on type ---
    if result.get("response_type") == "conversation":
        ChatMessage.objects.create(
            chat=chat,
            sender="assistant",
            message_type="conversation",
            content=result["conversation_details"]["response"]
        )
    elif result.get("response_type") == "recipe":
        # Recipe response
        recipe_details = result.get("recipe_details", {})

        # Extract ingredient names from the ingredients list
        ingredient_items = []
        for ingredient in recipe_details.get("ingredients", []):
            # Extract the item name (e.g., from "3 ripe bananas, mashed" -> "bananas")
            item = ingredient.split(' ')[-1]  # Get the last word as the ingredient item (this is basic)
            ingredient_items.append(item.lower())  # You can enhance this logic as needed

        # Create an Ai_model_logs record for the recipe
        Ai_model_logs.objects.create(
            email=user.email if user else None,  # Save the user's email if needed
            title=recipe_details.get("title", "Recipe"),
            overview=recipe_details.get("overview", ""),
            rating=recipe_details.get("rating", "N/A"),
            ingredients=recipe_details.get("ingredients", []),
            ingredient_items=ingredient_items,  # Now populated with ingredient item names
            instructions=recipe_details.get("instructions", ""),
        )

        # Save assistant message with recipe details
        ChatMessage.objects.create(
            chat=chat,
            sender="assistant",
            message_type="recipe",
            extra_data=recipe_details
        )
        profile.recipe_generate = int(profile.recipe_generate) + 1
        profile.save()
    elif result.get("response_type") == "error":
        error_details = result.get("error_details", {})
        
        # Create an error log in Ai_model_logs
        Ai_model_logs.objects.create(
            email=request.user.email,
            title=error_details.get("title", "Error"),
            overview=error_details.get("overview", ""),
            rating="N/A",  # Error logs might not have a rating
            ingredients=error_details.get("ingredients", []),
            ingredient_items=error_details.get("ingredient_items", []),
            instructions="",  # Error logs might not have instructions
        )

        # Save assistant message
        ChatMessage.objects.create(
            chat=chat,
            sender="assistant",
            message_type="error",
            extra_data=error_details
        )
    else:
        # fallback in case of unexpected AI response
        ChatMessage.objects.create(
            chat=chat,
            sender="assistant",
            message_type="error",
            extra_data={"overview": "Unexpected AI response", "raw": result}
        )

    chat.save()  # updates updated_at

    # return full structured response + chat id
    response_data = result
    response_data["chat_id"] = chat.id
    return Response(response_data, status=200)

@api_view(["GET"])
def get_chat_messages(request, chat_id):
    """Return full conversation messages (with pagination if needed)"""
    user = request.user
    try:
        chat = ChatSession.objects.get(id=chat_id, user=user)
    except ChatSession.DoesNotExist:
        return Response({"error": "Chat not found"}, status=404)

    messages = chat.messages.all().order_by("created_at")
    serializer = ChatMessageSerializer(messages, many=True)
    return Response({
        "chat_id": chat.id,
        "title": chat.title,
        "messages": serializer.data
    }, status=200)





class AiModelLogsListView(ListAPIView):
    queryset = Ai_model_logs.objects.all()  # Retrieve all records
    serializer_class = AiModelLogsSerializer