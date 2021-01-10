# Generated by Django 3.1.4 on 2021-01-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0036_user_profile_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.CharField(max_length=255)),
                ('tag', models.ManyToManyField(default=1, to='Maia.tag', verbose_name='Tag')),
            ],
        ),
    ]
