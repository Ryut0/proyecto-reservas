from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userprofile_reserva_creado_por'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancha',
            name='imagen',
            field=models.ImageField(
                blank=True, null=True,
                upload_to='canchas/',
                help_text='Foto de la cancha (opcional)'
            ),
        ),
    ]
