from django.db import models

# Create your models here.

class Paciente(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    personal_id = models.IntegerField(unique=True)
    contact_phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    birth_date = models.DateField()

    class Meta:
        db_table: 'Paciente'

        indexes = [
            models.Index(fields=['name', 'last_name']),
            models.Index(fields=['-birth_date']),

        ]


class Expediente(models.Model):
    id_paciente = models.OneToOneField(to=Paciente, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=15)
    grupo_sangre = models.CharField(max_length=15)
    peso = models.CharField(max_length=15)
    alergias = models.TextField()
    notas = models.TextField()

    class Meta:
        db_table: 'Expediente'

        indexes = [
            models.Index(fields=['id_paciente']),
            models.Index(fields=['grupo_sangre']),
        ]


class Consulta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    id_paciente = models.ForeignKey(to=Paciente, on_delete=models.CASCADE)
    id_expediente = models.ForeignKey(to=Expediente, on_delete=models.CASCADE)
    notas_consulta = models.TextField()

    class Meta:
        db_table: 'Consulta'

        indexes = [
            models.Index(fields=['id_paciente']),
            models.Index(fields=['id_expediente']),
        ]


class Examenes(models.Model):
    id_expediente = models.ForeignKey(to=Expediente, on_delete=models.CASCADE)

    class Meta:
        db_table: 'Examenes'
        verbose_name: 'Examenes'


class NotasAdjuntas(models.Model):
    id_expediente = models.ForeignKey(to=Expediente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table: 'NotasAdjuntas'
        verbose_name: 'Notas Adjuntas'


class Receta(models.Model):
    id_expediente = models.ForeignKey(to=Expediente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    id_paciente = models.ForeignKey(to=Paciente, on_delete=models.CASCADE)
    notas = models.TextField()

    class Meta:
        db_table: 'Receta'
        verbose_name: 'Receta'
        verbose_name_plural = 'Recetas'

        indexes = [
            models.Index(fields=['id_expediente']),
            models.Index(fields=['id_paciente']),
            models.Index(fields=['fecha']),
        ]


class DetalleReceta(models.Model):
    medicamentos = models.CharField(max_length=255)
    notas = models.CharField(max_length=255)

    class Meta:
        db_table: 'DetalleReceta'
        verbose_name: 'Detalle Receta'
        verbose_name_plural = 'Detalle Recetas'




