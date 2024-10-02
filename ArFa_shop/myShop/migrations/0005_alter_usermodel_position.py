# Generated by Django 5.0.6 on 2024-06-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0004_productmodel_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='position',
            field=models.IntegerField(choices=[(1, 'مدیر'), (2, 'پشتیبان'), (3, 'ثبت کالا'), (4, 'حسابدار'), (5, 'پست کالا')], verbose_name='سمت و پست کارمند'),
        ),
    ]
