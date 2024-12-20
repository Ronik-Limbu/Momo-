from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    message = models.TextField()    

class Foods(models.Model):  
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images') #pip install pillow
    desc=models.TextField()
    mark_price=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    descount_percent = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    price=models.DecimalField(default=0.00,max_digits=10,decimal_places=2,editable=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)  # Use string reference
    


    def save(self,*args, **kwargs):
        self.price=self.mark_price *(1-self.descount_percent/100)
        super().save(*args, **kwargs)
    
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            return sum(r.rating for r in ratings) / ratings.count()
        return 0
    
    def __str__(self) -> str:
        return self.name

    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, related_name='reviews')  # Use 'Foods' here
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, f'{i} Star') for i in range(1, 6)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.food.name}'