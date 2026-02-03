from django.db import models
from django.contrib.auth.models import User
from conf.settings import EXPIRATION_TIME_EMAIL
from products.models import Product

class VerifyCodes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    is_active=models.BooleanField(default=False)
    expiration_time=models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}: {self.code}"

    def save(self,*args,**kwargs):
        self.expiration_time=datetime.now()+timedelta(minutes=2)
        super().save(*args,**kwargs)



class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')

    def __str__(self):
        return f"{self.user.username} cart"

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    class Meta:
        unique_together=('cart','product')

    def __str__(self):
        return f"{self.product.title} "


class Order(models.Model):
    STATUS_CHOICES =(
        ('new','NEW'),
        ('paid','Paid'),
        ('shipped','SHIPPED'),
        ('cancelled','Cancelled'),
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='new')
    total_price=models.DecimalField(max_digits=12,decimal_places=2,default=0)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
