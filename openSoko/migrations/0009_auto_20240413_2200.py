# Generated by Django 3.0.5 on 2024-04-13 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openSoko', '0008_auto_20240413_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, default=b'bEYw0t3pd/xSxWu8eu7QlJAcmLFTIe6REKMiLdP7rllHaeEKnQbZs1KAYfNaxEezmSAgMDpM8cIfj+pr3TDgCQ==', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code_confirm',
            field=models.CharField(blank=True, default='4d6babb4d2617a06b1204276a3f1680d6b55d3838e5bac11da6ce428ead1aaf0', max_length=20, null=True),
        ),
    ]
