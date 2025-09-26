from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    # your existing URLs
    path('hijack/', include('hijack.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
