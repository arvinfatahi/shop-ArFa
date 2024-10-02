# Generated by Django 5.0.6 on 2024-09-24 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0053_alter_advertisingmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='myShop.categorymodel', verbose_name='دسته بندی محصول'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='نام محصول'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='number',
            field=models.IntegerField(blank=True, default=1, verbose_name='تعداد محصول'),
        ),
    ]
