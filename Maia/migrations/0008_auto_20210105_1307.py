# Generated by Django 3.1.4 on 2021-01-05 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0007_auto_20210105_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='financial_data_provided',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='qualitative_data_provided',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='user_profile_updated',
            field=models.BooleanField(default=False),
        ),
    ]
