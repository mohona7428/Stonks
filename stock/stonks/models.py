from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    desc = models.TextField()

    def __str__(self):
        return self.name


class Stock(models.Model):
    uname = models.CharField(max_length=20, default="null")
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class Sell(models.Model):
    uname = models.CharField(max_length=20, default="null")
    ticker = models.CharField(max_length=10)
    buyPrice = models.FloatField()
    quantity = models.IntegerField(default=0)
    sellPrice = models.FloatField()
    sellDate = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20, default="2022-02")

    def __str__(self):
        return self.ticker


class Transaction(models.Model):
    uname = models.CharField(max_length=20, default="null")
    ticker = models.CharField(max_length=10)
    buyPrice = models.FloatField()
    quantity = models.IntegerField(default=0)
    buyDate = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20, default="2022-02")

    def __str__(self):
        return self.ticker

class Portfolio(models.Model):
    uname = models.CharField(max_length=20, default="null")
    ticker = models.CharField(max_length=10)
    buyPrice = models.FloatField()
    quantity = models.IntegerField(default=0)
    buyDate = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20, default="2022-01")

    def __str__(self):
        return self.ticker
    

class Balance(models.Model):
    uname = models.CharField(max_length=20, default="null")
    balance = models.FloatField(default=100000)

    def __str__(self):
        return self.uname


class Level(models.Model):
    uname = models.CharField(max_length=20, default="null")
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.uname