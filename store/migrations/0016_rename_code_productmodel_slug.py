# Generated by Django 5.0.2 on 2024-02-29 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_rename_slug_productmodel_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='code',
            new_name='slug',
        ),
    ]