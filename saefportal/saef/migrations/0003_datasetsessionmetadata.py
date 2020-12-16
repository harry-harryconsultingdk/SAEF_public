# Generated by Django 3.0.3 on 2020-08-19 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saef', '0002_jobsessionmetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatasetSessionMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_type', models.CharField(choices=[('SUCCEEDED', 'SUCCEEDED'), ('SUCCEEDED_ISSUE', 'SUCCEEDED_ISSUE'), ('FAILED', 'FAILED')], max_length=128)),
                ('dataset_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saef.DatasetSession')),
            ],
        ),
    ]
