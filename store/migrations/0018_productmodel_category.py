# Generated by Django 5.0.2 on 2024-03-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_productmodel_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='category',
            field=models.CharField(default='Intel', max_length=255),
            preserve_default=False,
        ),
    ]