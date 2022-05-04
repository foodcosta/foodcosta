from itertools import product
from django.db import models
 
# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=13)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.email

class Item(models.Model):
    name = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class Sub_Item(models.Model):
    main_item = models.ForeignKey(Item,on_delete=models.CASCADE)
    subitem_name = models.CharField(max_length=20)
    price = models.IntegerField()
    size = models.CharField(max_length=10,null=True,blank=True)
    pic = models.FileField(upload_to='Items',null=True,blank=True)
    
    def __str__(self):
        return self.subitem_name + '  >  ' + self.subitem_name
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    food = models.ForeignKey(Sub_Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user)


class Book(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pay_id = models.CharField(max_length=50,null=True,blank=True)
    amount = models.IntegerField(default=0)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return   ' >> ' + self.user.fname

class Order(models.Model):

    item  = models.ForeignKey(Sub_Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    deli = models.BooleanField(default=False)

    def __str__(self):
        return self.item.subitem_name
    