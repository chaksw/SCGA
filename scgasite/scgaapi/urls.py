from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScgaViewSet, LevelViewSet, TestPlanViewSet, TestExceptionViewSet

router = DefaultRouter()
router.register(r"scgas", ScgaViewSet, basename="scgas")
router.register(r"levels", LevelViewSet, basename="levels")
router.register(r"testplans", TestPlanViewSet, basename="testplans")
router.register(r"testexceptions", TestExceptionViewSet, basename="testexceptions")

urlpatterns = [
    path("", include(router.urls))
]
