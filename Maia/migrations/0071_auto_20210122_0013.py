# Generated by Django 3.1.4 on 2021-01-21 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0070_auto_20210121_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_financial_data_v2',
            name='return_on_equity',
            field=models.FloatField(default=0, verbose_name='Return on Equity'),
        ),
        migrations.AddField(
            model_name='user_financial_data_v2',
            name='shareholder_equity',
            field=models.FloatField(default=0, verbose_name='Shareholder Equity'),
        ),
        migrations.AddField(
            model_name='user_financial_data_v2',
            name='total_liability',
            field=models.FloatField(default=0, verbose_name='Total Liability'),
        ),
    ]
