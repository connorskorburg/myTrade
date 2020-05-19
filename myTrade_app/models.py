from django.db import models
import re
# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = "Please Enter a Valid First Name!"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Please Enter a Valid Last Name!"
        valid_email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not valid_email.match(post_data['email']):
            errors['email'] = "Please Enter a valid Email Address!"
        if len(post_data['username']) < 5:
            errors['username'] = "Please Enter a Valid Username!"
        if len(post_data['password']) < 8:
            errors['password'] = "Please Enter a Valid Password!"
        if post_data['password'] != post_data['conf_password']:
            errors['confirm_password'] = "Password and Confirm Password do not match!"
        return errors

    def log_validator(self, post_data):
        errors = {}
        
        if len(post_data['username']) < 5:
            errors['username'] = "Please Enter a Valid Username!"
        if len(post_data['password']) < 8:
            errors['password'] = "Please Enter a Valid Password!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=30)
    bio = models.CharField(max_length=255)
    avatar = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    account_balance = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # stocks = a list of stocks bought
    # posts = a list of posts uploaded by the user
    # comments = a list of comments uploaded by the user
    # liked_posts = a list of the posts the user liked
     

class Trade(models.Model):
    symbol = models.CharField(max_length=15)
    price_per_share = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    total_price = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    shares = models.IntegerField(default=0)
    stock_holder = models.ForeignKey(User, related_name="trades", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SoldTrade(models.Model):
    price_sold = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    shares_sold = models.IntegerField()
    total_price_gained = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    stock_holder = models.ForeignKey(User, related_name='sold_trades', on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, related_name='transactions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Post(models.Model):
    content = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    user_who_liked = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(max_length=255)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)