# Generated by Django 3.1.4 on 2021-01-08 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0022_auto_20210106_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_financial_data',
            name='quater',
            field=models.CharField(choices=[('Q1', 'Quater 1'), ('Q2', 'Quater 2')], default='Q1', max_length=50, verbose_name='Quater'),
        ),
    ]
