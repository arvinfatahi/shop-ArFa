# Generated by Django 5.0.6 on 2024-10-01 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0058_productmodel_slider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='slider',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='انتخاب اسلاید'),
        ),
    ]
