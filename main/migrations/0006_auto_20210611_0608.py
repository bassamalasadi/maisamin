# Generated by Django 3.1.4 on 2021-06-11 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210608_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.TextField(blank=True, null=True),
        ),
    ]