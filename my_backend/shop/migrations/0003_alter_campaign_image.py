# Generated by Django 5.0.6 on 2024-07-09 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='image',
            field=models.ImageField(upload_to='campaigns'),
        ),
    ]