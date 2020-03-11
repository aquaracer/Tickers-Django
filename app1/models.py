from django.db import models


class Tickers(models.Model):
    stock_name = models.CharField(max_length=50, db_index=True) # добавляем индексацию т.к. по данному полю часто производится поиск
    date = models.DateField() # добавляем индексацию т.к. по данному полю часто производится поиск
    close = models.CharField(max_length=30)
    volume = models.CharField(max_length=30)
    open = models.CharField(max_length=30)
    high = models.CharField(max_length=30)
    low = models.CharField(max_length=30)


class Insiders(models.Model):
    stock_name = models.CharField(max_length=50, db_index=True) # добавляем индексацию т.к. по данному полю часто производится поиск
    insider = models.CharField(max_length=100, db_index=True) # добавляем индексацию т.к. по данному полю часто производится поиск
    relation = models.CharField(max_length=30)
    last_date = models.DateField()
    transaction_type = models.CharField(max_length=30)
    owner_type = models.CharField(max_length=30)
    shares_traded = models.CharField(max_length=30)
    last_price = models.CharField(max_length=30)
    shares_held = models.CharField(max_length=30)
