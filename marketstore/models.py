from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    
    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Sale Pending'),
        ('sold', 'Sold'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiable = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selling_items')
    location = models.CharField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    views_count = models.IntegerField(default=0)
    is_sold = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.item.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def average_rating(self):
        ratings = self.received_ratings.all()
        if ratings:
            return sum(rating.score for rating in ratings) / len(ratings)
        return 0

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='messages')
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class UserRating(models.Model):
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_ratings')
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    score = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('rated_user', 'rater')
    
    def __str__(self):
        return f"Rating for {self.rated_user.username} by {self.rater.username}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorited_by')
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'item')
    
    def __str__(self):
        return f"{self.user.username} favorited {self.item.title}"
