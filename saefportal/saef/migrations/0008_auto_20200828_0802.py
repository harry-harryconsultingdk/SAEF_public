# Generated by Django 3.0.5 on 2020-08-28 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saef', '0007_merge_20200828_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dataset_extraction_table',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
