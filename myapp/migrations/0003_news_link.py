# Generated by Django 2.1.5 on 2021-09-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20210917_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='link',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
    ]
