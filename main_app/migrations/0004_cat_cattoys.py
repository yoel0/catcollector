# Generated by Django 3.1.1 on 2020-09-22 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_cattoy'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='cattoys',
            field=models.ManyToManyField(to='main_app.CatToy'),
        ),
    ]
