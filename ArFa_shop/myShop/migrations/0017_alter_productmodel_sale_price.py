# Generated by Django 5.0.6 on 2024-06-26 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0016_alter_productmodel_is_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True, verbose_name='قیمت تخفیف خورده'),
        ),
    ]
