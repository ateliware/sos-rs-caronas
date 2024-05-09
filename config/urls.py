from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

API_VERSION = "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_VERSION, include("apps.core.urls")),
    path(API_VERSION, include("apps.address_manager.urls")),
    path(API_VERSION, include("apps.term_manager.urls.api_urls")),
    path(API_VERSION, include("apps.ride_manager.urls.api_urls")),
]

if settings.DEBUG:
    # Insert API Documentation on debug mode
    urlpatterns.extend(
        [
            path(
                f"{API_VERSION}schema/",
                SpectacularAPIView.as_view(),
                name="schema",
            ),
            path(
                f"{API_VERSION}swagger/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger-ui",
            ),
        ]
    )
admin.site.site_header = "SOS RS Caronas"
admin.site.index_title = "Recursos disponíveis"
admin.site.site_title = "SOS RS Caronas"
