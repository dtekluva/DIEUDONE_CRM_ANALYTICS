# Generated by Django 3.1.1 on 2021-05-28 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_attempt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
