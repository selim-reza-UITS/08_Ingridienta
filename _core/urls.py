from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from _core.handle404Views import (custom_400_view, custom_403_view,
                                  custom_404_view, custom_500_view)
from _core.settings.base import DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Name",
        default_version="v1",
        description="API documentation for user authentication and management",
        contact=openapi.Contact(email="your@email.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# No more urls will be add or remove from here
urlpatterns = [
    path('admin/', admin.site.urls),
    # 
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # 
    path("api/v1/",include("coreapi.api_endpoints")),
    path("test/api/v1/",include("coreapi.test_endpoints")),
]
# go to coreapi if any urls need to be added

urlpatterns = format_suffix_patterns(urlpatterns)
handler404 = custom_404_view
handler500 = custom_500_view
handler403 = custom_403_view
handler400 = custom_400_view