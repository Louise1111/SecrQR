# Generated by Django 5.0.3 on 2024-03-21 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Generate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('qr_code', models.ImageField(blank=True, upload_to='qrcodes/')),
                ('date', models.DateField(auto_now_add=True)),
                ('app_prefix', models.CharField(default='SECQR_APP by LOUISE,MARA, HECTOR', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('result', models.CharField(blank=True, max_length=20)),
                ('scanned_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
