# Generated by Django 3.0.5 on 2023-12-21 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duka', '0003_auto_20231109_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=200),
        ),
    ]