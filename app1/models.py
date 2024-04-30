from django.db import models

# Create your models here.


class UsersManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 charters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 charters'    
        if len(post_data['password1']) < 8:
            errors['password1'] = 'Password should be at least 8 charters'
            
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    
    
    objects = UsersManger()
    
    


class TripManger(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['destination']) < 2:
            errors['destination'] = 'destination should be at least 2 charters'
        if len(post_data['Itinerary']) > 50:
            errors['Itinerary'] = 'Itinerary should be less than 50 charters'    
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    Itinerary = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    travelers = models.ManyToManyField(User, related_name='travelers')
    
    objects = TripManger()
