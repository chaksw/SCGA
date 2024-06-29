from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScgaViewSet, LevelViewSet, TestPlanViewSet, TestExceptionViewSet, LvTotalCoverageViewSet, SCGAModuleViewSet, SCGAFunctionViewSet, CoverageViewSet, CoveredViewSet, totalViewSet, DefectClassificationViewSet, UncoverageViewSet, UploadSCGAsView

# router basename-list, basename-detail will be generated automatically
router = DefaultRouter()
router.register(r"scgas", ScgaViewSet, basename="scgas")
router.register(r"levels", LevelViewSet, basename="levels")
router.register(r"testplans", TestPlanViewSet, basename="testplans")
router.register(r"testexceptions", TestExceptionViewSet, basename="testexceptions")
router.register(r"lvTotalCoverages", LvTotalCoverageViewSet, basename="lvTotalCoverages")
router.register(r"modules", SCGAModuleViewSet, basename="modules")
router.register(r"functions", SCGAFunctionViewSet, basename="functions")
router.register(r"coverages", CoverageViewSet, basename="coverages")
router.register(r"covereds", CoveredViewSet, basename="covereds")
router.register(r"totals", totalViewSet, basename="totals")
router.register(r"defectclassifications", DefectClassificationViewSet, basename="defectclassifications")
router.register(r"uncoverages", UncoverageViewSet, basename="uncoverages")

urlpatterns = [
    path("", include(router.urls)),
    path('upload-scgas/', UploadSCGAsView.as_view(), name='upload-scgas')
]
