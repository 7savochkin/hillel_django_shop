# Generated by Django 3.2.15 on 2022-12-06 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='contact_form_email',
            field=models.EmailField(default='savochkinoleg@gmail.com', max_length=254),
        ),
    ]
