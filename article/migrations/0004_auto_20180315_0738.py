# Generated by Django 2.0.2 on 2018-03-15 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20180304_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summry',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
