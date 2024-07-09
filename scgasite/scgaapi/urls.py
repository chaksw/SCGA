from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
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

# loopup 的定义决定了在url中你将用什么在传递主键值
# 比如: lookup = 'scga', 那么在level中，其主键SCGA的键值就默认为scga_pk，具体在嵌套url中，运行get_queryset()时，
# 同时要注意的是，lookup 的值要与 level定义的 field值相同，否则会出现混乱

# Nested router
# scgas/{scga_id}/levels
scgas_router = routers.NestedSimpleRouter(router, r'scgas', lookup='scga')
scgas_router.register(r'levels', LevelViewSet, basename='scga-levels')

# scgas/{scga_id}/levels/{level_id}/testplans
# scgas/{scga_id}/levels/{level_id}/testexceptions
levels_router = routers.NestedSimpleRouter(scgas_router, r'levels', lookup='level')
levels_router.register(r'testplans', TestPlanViewSet, basename='level-testplans')
levels_router.register(r'testexceptions', TestExceptionViewSet, basename='level-testexceptions')

# scgas/{scga_id}/levels/{level_id}/testplans/{testplan_id}/modules
testplans_router = routers.NestedSimpleRouter(levels_router, r'testplans', lookup='test_plan')
testplans_router.register(r'tpmodules', TPModuleViewSet, basename='test_plan-modules')
testplans_router.register(r'lvtotalcoverages', LvTotalCoverageViewSet, basename='test_plan-lvtotalcoverages')

# scgas/{scga_id}/levels/{level_id}/testplans/{testplan_id}/tpmodules/{tpmodule_id}/tpfunctions
tpmodules_router = routers.NestedSimpleRouter(testplans_router, r'tpmodules', lookup='module')
tpmodules_router.register(r'tpfunctions', TPFunctionViewSet, basename='tpmodule-tpfunctions')

# scgas/{scga_id}/levels/{level_id}/testexceptions/{testexception_id}/modules
testexceptions_router = routers.NestedSimpleRouter(levels_router, r'testexceptions', lookup='test_exception')
testexceptions_router.register(r'temodules', TEModuleViewSet, basename='test_exception-modules')

# scgas/{scga_id}/levels/{level_id}/testexceptions/{testexception_id}/temodules/{temodule_id}/tefunctions
temodules_router = routers.NestedSimpleRouter(testexceptions_router, r'temodules', lookup='temodule')
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
