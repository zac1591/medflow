from django.contrib import admin
from .models import Paciente, Expediente

# Register your models here.

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'personal_id')

class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('id_paciente', 'date', 'gender', 'grupo_sangre', 'peso', 'alergias', 'notas')



admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Expediente, ExpedienteAdmin)