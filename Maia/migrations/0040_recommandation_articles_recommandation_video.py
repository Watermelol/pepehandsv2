# Generated by Django 3.1.4 on 2021-01-09 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maia', '0039_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommandation_Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Video_ID', models.CharField(max_length=255)),
                ('URL', models.CharField(max_length=255)),
                ('tag', models.ManyToManyField(default=1, to='Maia.tag', verbose_name='Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Recommandation_Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Description', models.TextField(blank=True)),
                ('Site_Name', models.CharField(max_length=50)),
                ('URL', models.CharField(max_length=255)),
                ('tag', models.ManyToManyField(default=1, to='Maia.tag', verbose_name='Tag')),
            ],
        ),
    ]
