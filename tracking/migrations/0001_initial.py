# Generated by Django 3.2.15 on 2022-10-25 13:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('method', models.CharField(max_length=16)),
                ('url', models.CharField(max_length=255)),
                ('data', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
