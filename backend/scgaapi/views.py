from django.core.files.uploadedfile import UploadedFile
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters
import pickle
import json
import utils

from .models import Scga, Level, TestPlan, TestException, LvTotalCoverage, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage
from .serializers import ScgaSerializer, LevelSerializer, TestPlanSerializer, TestExceptionSerializer, LvTotalCoverageSerializer, TPModuleSerializer, TEModuleSerializer, TPFunctionSerializer, TEFunctionSerializer, CoverageSerializer, CoveredSerializer, totalSerializer, DefectClassificationSerializer, UncoverageSerializer
# Create your views here.

# get_queryset() will be called for access of url (GET())
# perform_create will be called for creation of data (POST()), it will execute in .create() once is_valid() return true
# pk is more general. When you define a custom primary key field in a model, pk will always refer to this custom primary key, whereas id is the default field name.

class ScgaFilter(filters.FilterSet):
    baseline = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Scga
        fields = ['baseline']


class ScgaViewSet(viewsets.ModelViewSet):
    queryset = Scga.objects.all()
    serializer_class = ScgaSerializer
    # 在 DRF 原有的配置中
    # filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    # 现基于 django-filter 进行新的配置
    # 记得元组单个数据都是要加逗号 ,
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScgaFilter



class LevelViewSet(viewsets.ModelViewSet):
    # query is all the object of scga
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def get_queryset(self):
        scga_id = self.kwargs.get('scga_pk')
        return Level.objects.filter(scga_id=scga_id)
        # return Level.objects.filter(scga_id=self.kwargs['scga_pk'])

    def perform_create(self, serializer):
        scga_id = self.request.data.get('scga')
        if not scga_id:
            raise ValidationError({'scga': 'This field is required'})
        try:
            scga = Level.objects.get(pk=scga_id)
        except Scga.DoesNotExist:
            raise ValidationError({'scga': 'SCGA does not exist'})
        # scga_id = self.kwargs.get('scga_pk')
        # scga = Level.objects.get(pk=scga_id)
        # scga = Level.objects.get(pk=self.kwargs['scga_pk'])
        serializer.save(scga=scga)


class TestPlanViewSet(viewsets.ModelViewSet):
    # query is all the object of scga
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer

    def get_queryset(self):
        level_id = self.kwargs.get('level_pk')
        return TestPlan.objects.filter(level_id=level_id)
        # return TestPlan.objects.filter(level_id=self.kwargs['level_pk'])

    def create(self, request, *args, **kwargs):
        # 添加调试日志
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            print(f"Error while save test plan data: {e}")
            return Response({"error detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        for test_plan in TestPlan.objects.all():
            print(test_plan.sheet_name)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # level_id = self.kwargs.get('level_pk')
        # level = TestPlan.objects.get(pk=level_id)
        level = TestPlan.objects.get(pk=self.kwargs['level_pk'])
        serializer.save(level=level)





class TestExceptionViewSet(viewsets.ModelViewSet):
    queryset = TestException.objects.all()
    serializer_class = TestExceptionSerializer

    def get_queryset(self):
        level_id = self.kwargs.get('level_pk')
        return TestException.objects.filter(level_id=level_id)
        # return TestException.objects.filter(level_id=self.kwargs['level_pk'])

    def create(self, request, *args, **kwargs):
        # 添加调试日志
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # level_id = self.kwargs.get('level_pk')
        # level = TestException.objects.get(pk=level_id)
        level = TestException.objects.get(pk=self.kwargs['level_pk'])
        serializer.save(level=level)


class LvTotalCoverageViewSet(viewsets.ModelViewSet):
    queryset = LvTotalCoverage.objects.all()
    serializer_class = LvTotalCoverageSerializer

    def get_queryset(self):
        test_plan_id = self.kwargs.get('test_plan_pk')
        return LvTotalCoverage.objects.filter(test_plan_id=test_plan_id)
        # return LvTotalCoverage.objects.filter(test_plan_id=self.kwargs['test_plan_pk'])

    def perform_create(self, serializer):
        testplan = LvTotalCoverage.objects.get(pk=self.kwargs['test_plan_pk'])
        serializer.save(test_plan=testplan)

class TPModuleViewSet(viewsets.ModelViewSet):
    queryset = SCGAModule.objects.all()
    serializer_class = TPModuleSerializer

    def get_queryset(self):
        test_plan_id = self.kwargs.get('test_plan_pk')
        return SCGAModule.objects.filter(test_plan_id=test_plan_id)
        # return SCGAModule.objects.filter(test_plan_id=self.kwargs['test_plan_pk'])

    def perform_create(self, serializer):
        testplan = SCGAModule.objects.get(pk=self.kwargs['test_plan_pk'])
        serializer.save(test_plan=testplan)




class TEModuleViewSet(viewsets.ModelViewSet):
    queryset = SCGAModule.objects.all()
    serializer_class = TEModuleSerializer

    def get_queryset(self):
        test_exception_id = self.kwargs.get('test_exception_pk')
        return SCGAModule.objects.filter(test_exception_id=test_exception_id)
        # return SCGAModule.objects.filter(test_exception_id=self.kwargs['test_exception_pk'])

    def perform_create(self, serializer):
        testexception = SCGAModule.objects.get(pk=self.kwargs['test_exception_pk'])
        serializer.save(test_exception=testexception)


class TPFunctionViewSet(viewsets.ModelViewSet):
    queryset = SCGAFunction.objects.all()
    serializer_class = TPFunctionSerializer

    def get_queryset(self):
        temodule_id = self.kwargs.get('module_pk')
        return SCGAFunction.objects.filter(module_id=temodule_id)
        # return SCGAFunction.objects.filter(module_id=self.kwargs['module_pk'])

    def perform_create(self, serializer):
        tpmodule = SCGAFunction.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=tpmodule)


class TEFunctionViewSet(viewsets.ModelViewSet):
    queryset = SCGAFunction.objects.all()
    serializer_class = TEFunctionSerializer

    def get_queryset(self):
        temodule_id = self.kwargs.get('module_pk')
        return SCGAFunction.objects.filter(module_id=temodule_id)
        # return SCGAFunction.objects.filter(module_id=self.kwargs['module_pk'])

    def perform_create(self, serializer):
        temodule = SCGAFunction.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=temodule)


class CoverageViewSet(viewsets.ModelViewSet):
    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer

    def get_queryset(self):
        tpfunction_id = self.kwargs.get('function_pk')
        return Coverage.objects.filter(function_id=tpfunction_id)
        # return Coverage.objects.filter(function_id=self.kwargs['tpfunction_id'])

    def perform_create(self, serializer):
        tpfunction = Coverage.objects.get(pk=self.kwargs['function_pk'])
        serializer.save(function=tpfunction)


class CoveredViewSet(viewsets.ModelViewSet):
    queryset = Covered.objects.all()
    serializer_class = CoveredSerializer

    def get_queryset(self):
        tpfunction_id = self.kwargs.get('function_pk')
        return Covered.objects.filter(function_id=tpfunction_id)
        # return Coverage.objects.filter(function_id=self.kwargs['tpfunction_id'])

    def perform_create(self, serializer):
        tpfunction = Covered.objects.get(pk=self.kwargs['function_pk'])
        serializer.save(function=tpfunction)


class totalViewSet(viewsets.ModelViewSet):
    queryset = total.objects.all()
    serializer_class = totalSerializer

    def get_queryset(self):
        tpfunction_id = self.kwargs.get('function_pk')
        return total.objects.filter(function_id=tpfunction_id)
        # return Coverage.objects.filter(function_id=self.kwargs['tpfunction_id'])

    def perform_create(self, serializer):
        tpfunction = total.objects.get(pk=self.kwargs['function_pk'])
        serializer.save(function=tpfunction)


class DefectClassificationViewSet(viewsets.ModelViewSet):
    queryset = DefectClassification.objects.all()
    serializer_class = DefectClassificationSerializer

    def get_queryset(self):
        tpfunction_id = self.kwargs.get('function_pk')
        return DefectClassification.objects.filter(function_id=tpfunction_id)
        # return Coverage.objects.filter(function_id=self.kwargs['tpfunction_id'])

    def perform_create(self, serializer):
        tpfunction = DefectClassification.objects.get(pk=self.kwargs['function_pk'])
        serializer.save(function=tpfunction)


class UncoverageViewSet(viewsets.ModelViewSet):
    queryset = Uncoverage.objects.all()
    serializer_class = UncoverageSerializer

    def get_queryset(self):
        tefunction_id = self.kwargs.get('function_pk')
        return Uncoverage.objects.filter(function_id=tefunction_id)
        # return Coverage.objects.filter(function_id=self.kwargs['tpfunction_id'])

    def perform_create(self, serializer):
        tefunction = Uncoverage.objects.get(pk=self.kwargs['function_pk'])
        serializer.save(function=tefunction)

    
def serializerScgaPkl(scga_data):
    try:
        if isinstance(scga_data, list):
            if not all(isinstance(item, dict) for item in scga_data):
                return {"detail": "Invalid data format. Excepted a list of scga dictrionaries.", 'status': status.HTTP_400_BAD_REQUEST}
            for item in scga_data:
                serializer = ScgaSerializer(data=item)
                if serializer.is_valid(raise_exception=True):
                    # serializer.save() is ensentially calling .create() or .update() method defined in Serializer class
                    # 1. in case the primary key of request data not match with any created data, the .create() method will be call to create a new object.
                    # 2. in case the primary key of request data already exsit in created data, the .update() methode will be call to update the corresponding data object
                    serializer.save()
                else:
                    return {'detail': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
        elif isinstance(scga_data, dict):
            serializer = ScgaSerializer(data=scga_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return {'detail': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}
        return {'detail': "SCGAs uploaded successfully", 'status': status.HTTP_201_CREATED}
    except Exception as e:
        return {'detail': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR}

class UploadSCGAsView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        info = {
            "project": data['project'],
            "function": data['function'],
            "current": data['current'],
        }
        # print(data)
        if 'path' in data and data['path']: # handle multiple scgas
                SCGAs_process = utils.SCGAs(data['path'], 1, info)
                SCGAs_process.post_SCGAs(data['path'], 1, info)
                if response:
                    if response['result'] == 'success':
                        response = serializerScgaPkl(SCGAs_process.SCGAs)
                        return Response(response['detail'], status=response['status'])
                    elif response['result'] == 'error':
                        return Response(response['detail'], status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        elif 'file' in data and data['file']:  # handle one file object 
            file_ =  data['file']
            response = None
            # print(file_)
            # file_ = request.FILES.get('file')
            # print("file: ", file_)
            if not file_ or not isinstance(file_, UploadedFile):
                return Response({"detail": "No file uploaded or wrong file type."}, status=status.HTTP_400_BAD_REQUEST)
            elif file_.name.endswith('.xlsm'):
                scga = utils.SCGA(file_, info)
                scga.read_scga()
                response = serializerScgaPkl(scga.scga_dict)
                # response = scgaUtil.post_SCGAs()
            elif file_.name.endswith('.pkl'):
                scga_data = pickle.load(file_)
                response = serializerScgaPkl(scga_data) # parser scga pkl file
            return Response(response['detail'], status=response['status'])
        else:
            return Response({"detail": "Invalid file format. Please upload a .pkl or .xlsm file."}, status=status.HTTP_400_BAD_REQUEST)
                

