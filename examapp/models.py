from django.db import models
from datetime import datetime, timedelta
import bcrypt
NOW = str(datetime.now())


class PlanManager(models.Manager):
    def planvalidator(self,form):
        errors={}
        print (form)
        if len(form['destination'])<1:
            errors['destination'] = "Please enter a valid destination."
        if len(form['description'])<1:
            errors['description'] = "Please enter a valid description."
        if len(form['travelstart'])<1:
            errors['travelstart']="Please enter a valid start date."
        elif form["travelstart"] < NOW:
            errors['travelstart'] = "Start Date must be in the future." 
        if len(form['travelend'])<1:
            errors['travelend']="Please enter a valid end date."
        elif form["travelend"] < form["travelstart"]:
            errors['travelend'] = "Planned end date must be greater than start date."                
        return errors


    

class UserManager(models.Manager):
    
    def regvalidator(self,form):
        errors={}
        print (form)
        if len(form['name'])<3:
            errors['name'] = "Name must contain at least 3 letters."
        if len(form['username'])<3:
            errors['username'] = "Username must contain at least 3 lettes."
        elif User.objects.filter(username=form["username"]):
            errors['username'] = "username already in database, please login."        
        if not form['password']:
            errors['password'] = "Please enter a password."
        elif len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if not form['confirmpass']:
            errors['confirmpass'] = "Please enter a confirm password."
        elif form['confirmpass'] != form['password']:
            errors['confirmpass'] = "Passwords must match."
        return errors

    def loginValidator(self, form):
        errors = {}

        if not form['username']:
            errors['username'] = "Please enter username."
        elif not User.objects.filter(username=form["username"]):
            errors['username'] = "Username not found. Please register."
        else:
            user_list = User.objects.filter(username=form["username"])
            user = user_list[0]
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors['password'] = "Wrong password."
            if not form['password']:
                errors['password'] = "Please enter a password."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __repr__(self):
        return f"User object: {self.name}({self.id})"


class Plan(models.Model):
    destination= models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    travelstart=models.DateField()
    travelend=models.DateField()
    added_by = models.ForeignKey(User, related_name="plans_added", on_delete=models.CASCADE)
    users=models.ManyToManyField(User, related_name="plans")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=PlanManager()
    def __repr__(self):
        return f"<Plan object: {self.destination}({self.id})>"
