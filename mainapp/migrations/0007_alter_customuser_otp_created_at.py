# Generated by Django 4.2.6 on 2023-10-16 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_rename_date_todomodel_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='otp_created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
