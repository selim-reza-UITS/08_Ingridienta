import os
from typing import Dict, List, Optional, Literal

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# --- Configuration ---
load_dotenv()

# ==============================================================================
# 1. PYDANTIC SCHEMAS
# ==============================================================================


class Recipe(BaseModel):
    title: str = Field(description="The recipe title.")
    overview: str = Field(
        description="A brief, engaging 1-2 sentence description of the dish.",
        alias="overview/details",
    )
    rating: str = Field(
        description="A string representing a rating out of 5, like '4.7/5'."
    )
    ingredients: List[str] = Field(
        description="A list of strings, with each string being one ingredient AND its quantity."
    )
    ingredient_items: List[str] = Field(
        description="A list of strings containing ONLY the names of the ingredients, without quantities.",
        alias="ingrediants items",
    )
    instructions: str = Field(
        description="A single string containing detailed step-by-step instructions. Use '\\n' for new lines between steps."
    )


class ConversationalResponse(BaseModel):
    response: str = Field(
        description="The helpful, conversational text response to the user's input."
    )
    items_list: Optional[List[str]] = Field(
        None,
        description="An optional list of items if the user specifically asks for a list (e.g., 'just the ingredient names').",
    )


# --- NEW: Schema for the error response ---
class ErrorResponse(BaseModel):
    """Schema for reporting why a recipe could not be generated."""

    title: str = Field(
        description="A title for the error, e.g., 'Recipe Request Invalid'."
    )
    overview: str = Field(
        description="A clear explanation of why the recipe could not be generated due to a contradiction or impossibility."
    )
    ingredient_items: List[str] = Field(
        description="A list of ingredient names that the user mentioned in their request.",
        alias="ingrediants items",
    )


# --- UPDATED: Main schema now includes the 'error' type and details ---
class RecipeBotOutput(BaseModel):
    """The final, top-level schema for the bot's output."""

    response_type: Literal["recipe", "conversation", "error"] = Field(
        description="The type of response generated."
    )
    recipe_details: Optional[Recipe] = Field(
        None, description="The detailed recipe, if one was generated."
    )
    conversation_details: Optional[ConversationalResponse] = Field(
        None, description="The conversational response, if one was generated."
    )
    error_details: Optional[ErrorResponse] = Field(
        None, description="Details about the error, if a recipe request was invalid."
    )


# ==============================================================================
# 2. THE SPECIALIST AGENT
# ==============================================================================


class RecipeAgent:
    def __init__(self):
        llm = ChatOpenAI(
            model="gpt-4o", temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # --- UPDATED: The system prompt now includes the new error handling logic ---
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a versatile recipe and conversational assistant. Your task is to analyze the user's input and conversation history to determine the correct response. Your output MUST be a single, valid JSON object that conforms to the `RecipeBotOutput` schema.
**Decision Logic (follow this exact order):**
1.  **Generate an Error (`response_type: "error"`)**: 
    FIRST, carefully check if the recipe request contains any contradictions, impossibilities, or nonsensical elements.
    
    When to use this:
    - Religious/dietary contradictions (e.g., "Islamic pork recipe" - pork is haram in Islam)
    - Impossible combinations (e.g., "vegan beef steak" - beef cannot be vegan)
    - Physically impossible requests (e.g., "recipe that cooks in -10 minutes")
    - Nonsensical ingredients (e.g., "concrete sandwich recipe")
    
    What to do:
    - Set `response_type` to "error"
    - Fill ONLY the `error_details` field
    - In `title`: Write a clear error title like "Recipe Request Invalid"
    - In `overview`: Explain in simple terms WHY this request is impossible or contradictory
    - In `ingredient_items`: List any actual ingredients the user mentioned (even problematic ones)
    - DO NOT fill `recipe_details` or `conversation_details`
2.  **Generate a Recipe (`response_type: "recipe"`)**: 
    Use this ONLY when the user is explicitly asking for a NEW recipe AND the request is valid.
    
    Clear signs the user wants a new recipe:
    - "Give me a recipe for..."
    - "How do I make..."
    - "Can you show me how to cook..."
    - "I want a recipe for..."
    
    What to do:
    - Set `response_type` to "recipe"
    - Fill ONLY the `recipe_details` field with complete recipe information
    - Make sure ALL fields are filled: title, overview, rating, ingredients, ingredient_items, instructions
    - Write step-by-step instructions that a beginner can easily follow
    - Use clear measurements and cooking terms
    - DO NOT fill `error_details` or `conversation_details`
3.  **Have a Conversation (`response_type: "conversation"`)**: 
    Use this for EVERYTHING ELSE. This is your default choice when not generating recipes or errors.
    
    When to use this:
    - Greetings ("hello", "hi", "good morning")
    - Questions about existing recipes already discussed
    - General cooking questions
    - Requests for cooking tips or advice
    - Follow-up questions about recipes from conversation history
    - Requests for ingredient substitutions
    - Storage or preparation questions
    
    What to do:
    - Set `response_type` to "conversation"
    - Fill ONLY the `conversation_details` field
    - In `response`: Write a helpful, friendly response
    - If user asks for a simple list (like "just the ingredient names"), put the list in `items_list`
    - When answering follow-ups, refer to the conversation history to give contextual answers
    - DO NOT create new recipes in conversation mode
    - DO NOT fill `recipe_details` or `error_details`
**Important Rules:**
- Always fill exactly ONE of the three detail fields (recipe_details, conversation_details, or error_details)
- Never fill multiple detail fields at the same time
- When in doubt between recipe and conversation, choose conversation
- Always be helpful and beginner-friendly in your responses""",
                ),
                (
                    "human",
                    """Here is the conversation history:
<history>
{history}
</history>
Analyze the latest user message and generate the appropriate response based on your decision logic.
Latest User Message: '{user_input}'""",
                ),
            ]
        )
        self.chain = prompt | llm.with_structured_output(
            RecipeBotOutput, method="function_calling"
        )

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        if not history:
            return "No history yet."
        formatted_lines = []
        for message in history:
            sender = message.get("sender", "unknown").capitalize()
            content = message.get("content", "")
            formatted_lines.append(f"{sender}: {content}")
        return "\n".join(formatted_lines)

    def run(
        self, user_input: str, conversation_history: List[Dict[str, str]]
    ) -> RecipeBotOutput:
        history_str = self._format_history(conversation_history)
        return self.chain.invoke({"history": history_str, "user_input": user_input})


# ==============================================================================
# 3. THE ORCHESTRATOR
# ==============================================================================


class RecipeOrchestrator:
    def __init__(self):
        self.recipe_agent = RecipeAgent()

    def run_analysis(self, user_input: str, conversation_history: List[Dict]) -> Dict:
        """Processes the user input against the conversation history and returns a structured dictionary."""
        try:
            structured_result = self.recipe_agent.run(
                user_input=user_input, conversation_history=conversation_history
            )
            return structured_result.model_dump(by_alias=True, exclude_none=True)
        except Exception as e:
            print(f"Error during analysis: {e}")
            error_details = str(e)
            if "OUTPUT_PARSING_FAILURE" in error_details:
                return {
                    "error": "Failed to process the request due to an invalid format from the model.",
                    "details": "The AI model's response was malformed and could not be parsed.",
                }
            return {"error": "An unexpected error occurred.", "details": error_details}


# ==============================================================================
# 4. REUSABLE FUNCTION (PUBLIC API ENTRY POINT)
# ==============================================================================


def get_recipe_response(user_input: str, conversation_history: List[Dict]) -> Dict:
    """
    Handles an incoming message, processes it, and returns the structured action.
    Args:
        user_input: The user's current message.
        conversation_history: A list of previous message dictionaries.

    Returns:
        A dictionary containing the full analysis and response.
    """
    if not user_input:
        return {"error": "User input cannot be empty."}

    orchestrator = RecipeOrchestrator()
    return orchestrator.run_analysis(
        user_input=user_input, conversation_history=conversation_history
    )
