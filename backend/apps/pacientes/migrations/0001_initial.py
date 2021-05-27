# Generated by Django 3.1.7 on 2021-05-27 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('notas_consulta', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleReceta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicamentos', models.CharField(max_length=255)),
                ('notas', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Detalle Recetas',
            },
        ),
        migrations.CreateModel(
            name='Examenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(max_length=15)),
                ('grupo_sangre', models.CharField(max_length=15)),
                ('peso', models.CharField(max_length=15)),
                ('alergias', models.TextField()),
                ('notas', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NotasAdjuntas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('personal_id', models.IntegerField(unique=True)),
                ('contact_phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('notas', models.TextField()),
                ('id_expediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.expediente')),
                ('id_paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente')),
            ],
            options={
                'verbose_name_plural': 'Recetas',
            },
        ),
        migrations.AddIndex(
            model_name='paciente',
            index=models.Index(fields=['name', 'last_name'], name='pacientes_p_name_2cae3a_idx'),
        ),
        migrations.AddIndex(
            model_name='paciente',
            index=models.Index(fields=['-birth_date'], name='pacientes_p_birth_d_79b38d_idx'),
        ),
        migrations.AddField(
            model_name='notasadjuntas',
            name='id_expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.expediente'),
        ),
        migrations.AddField(
            model_name='expediente',
            name='id_paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente'),
        ),
        migrations.AddField(
            model_name='examenes',
            name='id_expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.expediente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='id_expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.expediente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='id_paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente'),
        ),
        migrations.AddIndex(
            model_name='receta',
            index=models.Index(fields=['id_expediente'], name='pacientes_r_id_expe_8515b9_idx'),
        ),
        migrations.AddIndex(
            model_name='receta',
            index=models.Index(fields=['id_paciente'], name='pacientes_r_id_paci_a1bd59_idx'),
        ),
        migrations.AddIndex(
            model_name='receta',
            index=models.Index(fields=['fecha'], name='pacientes_r_fecha_be48ef_idx'),
        ),
        migrations.AddIndex(
            model_name='expediente',
            index=models.Index(fields=['id_paciente'], name='pacientes_e_id_paci_83800b_idx'),
        ),
        migrations.AddIndex(
            model_name='expediente',
            index=models.Index(fields=['grupo_sangre'], name='pacientes_e_grupo_s_df418f_idx'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['id_paciente'], name='pacientes_c_id_paci_600260_idx'),
        ),
        migrations.AddIndex(
            model_name='consulta',
            index=models.Index(fields=['id_expediente'], name='pacientes_c_id_expe_4744a4_idx'),
        ),
    ]
