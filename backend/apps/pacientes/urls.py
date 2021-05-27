from django.urls import path
from .views import Paciente_list

urlpatterns = [
    path('', Paciente_list.as_view(), name='pacientes'),
]