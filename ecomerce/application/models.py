from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = [
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CT', 'Chhattisgarh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HR', 'Haryana'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('JH', 'Jharkhand'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('MP', 'Madhya Pradesh'),
    ('MH', 'Maharashtra'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Odisha'),
    ('PB', 'Punjab'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    ('AN', 'Andaman and Nicobar Islands'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DL', 'Delhi'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Puducherry')
]

CATEGORY_CHOICES = (
    ("CR", "Curd"),
    ("ML", "Milk"),
    ("LS", "Lassi"),
    ("MS", "MilkShake"),
    ("PN", "Paneer"),
    ("GH", "Ghee"),
    ("CH", "Cheese"),
    ("IC", "Ice-Creams"),

)

class Products(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(verbose_name='Discount Price')
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    class Meta:
        verbose_name_plural = "Products"
        
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products, related_name='wishlisted_by')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart of {self.user.username}'

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total(self):
        return self.get_subtotal()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.title}'

    def get_total_price(self):
        return self.quantity * self.product.discounted_price
    

