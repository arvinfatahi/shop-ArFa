# Generated by Django 5.0.6 on 2024-06-25 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0012_alter_ticketmodel_receive_alter_ticketmodel_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='نام برند')),
                ('image', models.ImageField(upload_to='brandImage/', verbose_name='عکس')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برندها',
            },
        ),
    ]
