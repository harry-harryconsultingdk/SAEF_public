# Generated by Django 3.0.5 on 2020-08-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saef', '0005_auto_20200826_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetsession',
            name='degree_of_change',
            field=models.FloatField(null=True),
        ),
    ]
