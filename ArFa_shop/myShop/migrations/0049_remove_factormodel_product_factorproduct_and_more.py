# Generated by Django 5.0.6 on 2024-09-22 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0048_alter_ticketmodel_receive_alter_ticketmodel_send'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factormodel',
            name='product',
        ),
        migrations.CreateModel(
            name='FactorProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='تعداد محصول')),
                ('factor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myShop.factormodel', verbose_name='فاکتور')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myShop.productmodel', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'محصولات فاکتور',
                'verbose_name_plural': 'محصولات فاکتورها',
            },
        ),
        migrations.AddField(
            model_name='factormodel',
            name='product',
            field=models.ManyToManyField(through='myShop.FactorProduct', to='myShop.productmodel', verbose_name='محصول'),
        ),
    ]
