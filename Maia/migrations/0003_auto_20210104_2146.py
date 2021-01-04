# Generated by Django 3.1.4 on 2021-01-04 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0002_auto_20210104_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='address_1',
            field=models.CharField(default='-', max_length=255, verbose_name='Address 1'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='address_2',
            field=models.CharField(default='-', max_length=255, verbose_name='Address 2'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='city',
            field=models.CharField(default='-', max_length=1024, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='email',
            field=models.EmailField(default='-', max_length=254),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='first_name',
            field=models.CharField(default='-', max_length=255, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='last_name',
            field=models.CharField(default='-', max_length=255, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='zip_code',
            field=models.CharField(default='-', max_length=12, verbose_name='ZIP / Postal code'),
        ),
    ]
