# Generated by Django 2.2.1 on 2019-06-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190619_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
