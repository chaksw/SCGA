from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested  import routers
from .views import ScgaViewSet, LevelViewSet, TestPlanViewSet, TestExceptionViewSet, LvTotalCoverageViewSet, TPModuleViewSet, TEModuleViewSet, TPFunctionViewSet, TEFunctionViewSet, CoverageViewSet, CoveredViewSet, totalViewSet, DefectClassificationViewSet, UncoverageViewSet, UploadSCGAsView

# router basename-list, basename-detail will be generated automatically
router = DefaultRouter()
router.register(r"scgas", ScgaViewSet, basename="scgas")
router.register(r"levels", LevelViewSet, basename="levels")
router.register(r"testplans", TestPlanViewSet, basename="testplans")
router.register(r"testexceptions", TestExceptionViewSet, basename="testexceptions")
router.register(r"lvtotalcoverages", LvTotalCoverageViewSet, basename="lvtotalcoverages")
router.register(r"tpmodules", TPModuleViewSet, basename="tpmodules")
router.register(r"temodules", TEModuleViewSet, basename="temodules")
router.register(r"tpfunctions", TPFunctionViewSet, basename="tpfunctions")
router.register(r"tefunctions", TEFunctionViewSet, basename="tefunctions")
router.register(r"coverages", CoverageViewSet, basename="coverages")
router.register(r"covereds", CoveredViewSet, basename="covereds")
router.register(r"totals", totalViewSet, basename="totals")
router.register(r"defectclassifications", DefectClassificationViewSet, basename="defectclassifications")
router.register(r"uncoverages", UncoverageViewSet, basename="uncoverages")

# Nested router
# scgas/{scga_id}/levels
scgas_router = routers.NestedSimpleRouter(router, r'scgas', lookup='scga')
scgas_router.register(r'levels', LevelViewSet, basename='scga-levels')

# levels/{level_id}/testplans
# levels/{level_id}/testexceptions
levels_router = routers.NestedSimpleRouter(router, r'levels', lookup='level')
levels_router.register(r'testplans', TestPlanViewSet, basename='level-testplans')
levels_router.register(r'testexceptions', TestExceptionViewSet, basename='level-testexceptions')

# testplans/{testplan_id}/modules
testplans_router = routers.NestedSimpleRouter(router, r'testplans', lookup='testplan')
testplans_router.register(r'tpmodules', TPModuleViewSet, basename='testplan-modules')
testplans_router.register(r'lvtotalcoverages', LvTotalCoverageViewSet, basename='testplan-lvtotalcoverages')

# testexceptions/{testexception_id}/modules
testexceptions_router = routers.NestedSimpleRouter(router, r'testexceptions', lookup='testexception')
testexceptions_router.register(r'temodules', TPModuleViewSet, basename='testexception-modules')

# testplans/{testplan_id}/tpmodules/{tpmodule_id}/tpfunctions
tpmodules_router = routers.NestedSimpleRouter(router, r'tpmodules', lookup='tpmodule')
tpmodules_router.register(r'tpfunctions', TPFunctionViewSet, basename='tpmodule-tpfunctions')

# testexceptions/{testexception_id}/temodules/{temodule_id}/tefunctions
temodules_router = routers.NestedSimpleRouter(router, r'temodules', lookup='temodule')
temodules_router.register(r'tefunctions', TEFunctionViewSet, basename='temodule-tefunctions')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(scgas_router.urls)),
    path("", include(levels_router.urls)),
    path("", include(testplans_router.urls)),
    path("", include(testexceptions_router.urls)),
    path("", include(tpmodules_router.urls)),
    path("", include(temodules_router.urls)),
    path('upload-scgas/', UploadSCGAsView.as_view(), name='upload-scgas')
]
