# Generated by Django 5.0.3 on 2024-04-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0008_alter_user_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="user",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True, default="default.png", null=True, upload_to="profiles/"
            ),
        ),
    ]