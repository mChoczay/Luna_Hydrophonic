# Generated by Django 5.0.3 on 2024-04-02 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crudapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HydrophonicSystem',
            new_name='HydroponicSystem',
        ),
        migrations.RenameField(
            model_name='hydroponicsystem',
            old_name='pH',
            new_name='ph',
        ),
    ]