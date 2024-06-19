from django.urls import path
from . import views

urlpatterns = [
    path("scgas/", views.ScgaListCreate.as_view(), name='scga-view-create'),
    path("scgas/<int:pk>/", views.ScgaRetrieveUpdateDestroy.as_view(),
         name='scga-view-update')
]
