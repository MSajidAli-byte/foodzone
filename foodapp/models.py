from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Table'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name_plural = 'Profile Table'
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/%Y/%m/%d")
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    # updated_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Category Table'

class Dish(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='dishes/%Y/%m/%d')
    ingredients = models.TextField()
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # updated_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Dish Table'

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=100, blank=True)
    payer_id = models.CharField(max_length=100, blank=True)
    ordered_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.customer.user.username}"

    class Meta:
        verbose_name_plural = 'Order Table'