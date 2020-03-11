# Generated by Django 3.0.3 on 2020-02-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insiders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insider', models.CharField(max_length=100)),
                ('relation', models.CharField(max_length=30)),
                ('last_date', models.DateField()),
                ('transaction_type', models.CharField(max_length=30)),
                ('owner_type', models.CharField(max_length=30)),
                ('shares_traded', models.IntegerField()),
                ('last_price', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tickers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('close_last', models.CharField(max_length=30)),
                ('volume', models.IntegerField()),
                ('open', models.CharField(max_length=30)),
                ('high', models.CharField(max_length=30)),
                ('low', models.CharField(max_length=30)),
            ],
        ),
    ]
