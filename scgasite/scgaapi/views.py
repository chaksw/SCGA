from django.shortcuts import render
from rest_framework import generics, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Scga, Level, TestPlan, TestException, LvTotalCoverage, SCGAModule, SCGAFunction, Coverage, Covered, total, DefectClassification, Uncoverage
from .serializers import ScgaSerializer, LevelSerializer, TestPlanSerializer, TestExceptionSerializer, LvTotalCoverageSerializer, SCGAModuleSerializer, SCGAFunctionSerializer, CoverageSerializer, CoveredSerializer, totalSerializer, DefectClassificationSerializer, UncoverageSerializer
from rest_framework.views import APIView
from django.core.files.uploadedfile import UploadedFile
import pickle
# Create your views here.


class ScgaViewSet(viewsets.ModelViewSet):
    queryset = Scga.objects.all()
    serializer_class = ScgaSerializer


class LevelViewSet(viewsets.ModelViewSet):
    # query is all the object of scga
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class TestPlanViewSet(viewsets.ModelViewSet):
    # query is all the object of scga
    queryset = TestPlan.objects.all()
    serializer_class = TestPlanSerializer

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
        serializer.save()


class TestExceptionViewSet(viewsets.ModelViewSet):
    queryset = TestException.objects.all()
    serializer_class = TestExceptionSerializer

    def create(self, request, *args, **kwargs):
        # 添加调试日志
        print("Received data:", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class LvTotalCoverageViewSet(viewsets.ModelViewSet):
    queryset = LvTotalCoverage.objects.all()
    serializer_class = LvTotalCoverageSerializer


class SCGAModuleViewSet(viewsets.ModelViewSet):
    queryset = SCGAModule.objects.all()
    serializer_class = SCGAModuleSerializer


class SCGAFunctionViewSet(viewsets.ModelViewSet):
    queryset = SCGAFunction.objects.all()
    serializer_class = SCGAFunctionSerializer


class CoverageViewSet(viewsets.ModelViewSet):
    queryset = Coverage.objects.all()
    serializer_class = CoverageSerializer


class CoveredViewSet(viewsets.ModelViewSet):
    queryset = Covered.objects.all()
    serializer_class = CoveredSerializer


class totalViewSet(viewsets.ModelViewSet):
    queryset = total.objects.all()
    serializer_class = totalSerializer


class DefectClassificationViewSet(viewsets.ModelViewSet):
    queryset = DefectClassification.objects.all()
    serializer_class = DefectClassificationSerializer


class UncoverageViewSet(viewsets.ModelViewSet):
    queryset = Uncoverage.objects.all()
    serializer_class = UncoverageSerializer


class UploadSCGAsView(APIView):
    def post(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        file = request.FILES.get('file')
        if not file or not isinstance(file, UploadedFile):
            return Response({"detail": "No file uploaded or wrong file type."}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.pkl'):
            return Response({"detail": "Invalid file format. Please upload a .pkl file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # load data from .pkl file
            data = pickle.load(file)
            if isinstance(data, list):
                if not all(isinstance(item, dict) for item in data):
                    return Response({"detail": "Invalid data format. Excepted a list of dictrionaries."}, status=status.HTTP_400_BAD_REQUEST)
                for item in data:
                    serializer = ScgaSerializer(data=item)
                    if serializer.is_valid():
                        # serializer.save() is ensentially calling .create() or .update() method defined in Serializer class
                        # 1. in case the primary key of request data not match with any created data, the .create() method will be call to create a new object.
                        # 2. in case the primary key of request data already exsit in created data, the .update() methode will be call to update the corresponding data object
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': "SCGAs uploaded successfully"}, status=status.HTTP_201_CREATED)
            elif isinstance(data, dict):
                serializer = ScgaSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class ScgaListCreate(generics.ListCreateAPIView):
#     # query is all the object of scga
#     queryset = Scga.objects.all()
#     serializer_class = ScgaSerializer

#     # override http methode delete()
#     def delete(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ScgaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Scga.objects.all()
#     serializer_class = ScgaSerializer
#     lookup_field = 'pk'  # primary key

# class TestPlanListCreate(generics.ListCreateAPIView):
#     # query is all the object of scga
#     queryset = TestPlan.objects.all()
#     serializer_class = TestPlanSerializer

#     # override http methode delete()
#     def delete(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TestPlanRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TestPlan.objects.all()
#     serializer_class = TestPlanSerializer
#     lookup_field = 'pk'  # primary key


# class TestExceptionListCreate(generics.ListCreateAPIView):
#     # query is all the object of scga
#     queryset = TestException.objects.all()
#     serializer_class = TestExceptionSerializer

#     # override http methode delete()
#     def delete(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TestExceptionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TestException.objects.all()
#     serializer_class = TestExceptionSerializer
#     lookup_field = 'pk'  # primary key
