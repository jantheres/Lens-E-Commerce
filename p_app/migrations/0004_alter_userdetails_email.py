# Generated by Django 5.0.4 on 2024-05-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0003_alter_userdetails_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
