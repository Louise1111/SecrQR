# Generated by Django 5.0.3 on 2024-04-25 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_alter_user_username"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlacklistedToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]