# Generated by Django 4.2.6 on 2023-10-13 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_todomodel_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todomodel',
            old_name='date',
            new_name='deadline',
        ),
    ]
