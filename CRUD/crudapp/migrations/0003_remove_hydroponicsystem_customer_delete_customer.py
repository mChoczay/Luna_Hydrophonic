# Generated by Django 5.0.3 on 2024-04-02 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0002_rename_hydrophonicsystem_hydroponicsystem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hydroponicsystem',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
