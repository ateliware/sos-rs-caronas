from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.term_manager.apis import TermAcceptanceViewSet, TermViewSet

router = DefaultRouter()

router.register(
    r"acceptance-terms",
    TermAcceptanceViewSet,
    basename="acceptance-terms",
)

urlpatterns = [
    path(
        "terms/",
        TermViewSet.as_view({"get": "retrieve"}),
        name="terms",
    ),
]

urlpatterns += router.urls
