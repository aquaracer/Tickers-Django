# Generated by Django 3.0.3 on 2020-02-28 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20200227_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='insiders',
            name='shares_held',
            field=models.CharField(default=11, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='insiders',
            name='stock_name',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='insiders',
            name='shares_traded',
            field=models.CharField(max_length=30),
        ),
    ]
