# Generated by Django 5.0.6 on 2024-08-22 15:54

from django.db import migrations
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0032_alter_commentmodel_published_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='published_comment',
            field=models.DateField(auto_now_add=True),
        ),
    ]
