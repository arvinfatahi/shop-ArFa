# Generated by Django 5.0.6 on 2024-10-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0057_alter_discountcodemodel_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='slider',
            field=models.BooleanField(blank=True, null=True, verbose_name='انتخاب اسلاید'),
        ),
    ]
