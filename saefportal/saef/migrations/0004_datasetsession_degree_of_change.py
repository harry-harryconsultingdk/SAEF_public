# Generated by Django 3.0.5 on 2020-08-26 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saef', '0003_datasetsessionmetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetsession',
            name='degree_of_change',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
