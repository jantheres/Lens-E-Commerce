from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Lense(models.Model):
    

    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=50)
    p_desc = models.TextField()
    p_quantity = models.PositiveIntegerField()
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_image = models.ImageField(upload_to='uploads')
    
    cat=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.p_name
    
    class Meta:
        db_table = 'p_app'


class UserDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    mobile_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class admin_login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)


class cart(models.Model):
    customer = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)



class CartProduct(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Lense, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "cart:" + str(self.cart.id) + "cartproduct:" + str(self.id)


ORDER_STATUS = (
    ("order recived", "order recived"),
    ("order processing", "order processing"),
    ("order on the way", "order on the way"),
    ("order completed", "order completed"),
    ("order cancelled", "order cancelled")
)


class Orders(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100,default="ssss")
    mobile  =models.CharField(max_length=50, default="45678")

    def __str__(self):
        return "order:" + str(self.id)
    

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Lense)

    def __str__(self):
        return f"Wishlist of {self.user.username}"

