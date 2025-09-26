

# 1️⃣ USER VIEW — only active packages
class ActiveSubscriptionListView(generics.ListAPIView):
    queryset = Subscription.objects.filter(status=True)
    serializer_class = SubcriptionsSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="List Active Subscriptions",
        operation_description="Returns a list of active subscription packages available to users.",
        responses={200: SubcriptionsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 2️⃣ ADMIN VIEW — list + create
class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubcriptionsSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List All Subscriptions (Admin)",
        operation_description="Returns all subscriptions, active and inactive.",
        responses={200: SubcriptionsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Subscription (Admin)",
        operation_description="Creates a new subscription package. Admin only.",
        request_body=SubcriptionsSerializer,
        responses={201: SubcriptionsSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubscriptionPartialUpdateView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionStatusUpdateSerializer  # only status is editable
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['patch']
    lookup_field = "package_id"  # use package_id from URL

    @swagger_auto_schema(
        operation_summary="Update Subscription Status (Admin)",
        operation_description="Updates the subscription status via query param. Only Admins can perform this.",
        request_body=None,
        responses={200: SubscriptionStatusUpdateSerializer}
    )
    def patch(self, request, *args, **kwargs):
        # Get the status from query parameters
        status_param = request.query_params.get("status", None)
        if status_param is None:
            return Response({"error": "Missing 'status' query parameter."}, status=400)

        # Convert string to boolean
        if status_param.lower() in ["true", "1", "yes"]:
            status_value = True
        elif status_param.lower() in ["false", "0", "no"]:
            status_value = False
        else:
            return Response({"error": "Invalid 'status' value. Must be true or false."}, status=400)

        # Update the object
        subscription = self.get_object()
        subscription.status = status_value
        subscription.save()

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)

class UserAdminDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithSubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    
    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request  # Add the request to the context
        return context