# Generated by Django 3.0.5 on 2024-04-13 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openSoko', '0004_auto_20240413_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='ordered_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, default=b'FEO0U+B+x6n71lbEJNCImELseLJwLJom3WYlPk5JRXMmXSMne1mYrefCwv/AgrkrhgIYTWX9pfvIcekL9LnasQ==', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code_confirm',
            field=models.CharField(blank=True, default='458bc738150b799ae0a38e652565d5e216f1e1dc1f1e9d261989610f40c29a4e', max_length=20, null=True),
        ),
    ]
