# Generated by Django 5.0.3 on 2024-03-21 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secQr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generate',
            name='app_prefix',
            field=models.CharField(default='SecQRapp', max_length=50),
        ),
        migrations.AlterField(
            model_name='scan',
            name='result',
            field=models.CharField(default='Unknown', max_length=20),
        ),
    ]
