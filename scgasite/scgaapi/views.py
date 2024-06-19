from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Scga
from .serializers import ScgaSerializer
from rest_framework.views import APIView
# Create your views here.


class ScgaListCreate(generics.ListCreateAPIView):
    # query is all the object of scga
    queryset = Scga.objects.all()
    serializer_class = ScgaSerializer

    # override http methode delete()
    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScgaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scga.objects.all()
    serializer_class = ScgaSerializer
    lookup_field = 'pk'  # primary key
