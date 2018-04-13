# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager (models.Manager):
    def regValidator (self, postData):
        errors = {
            'registration': []
        }
        pass
        #verfies the length of string entered in the name field is >= 2
        if len(postData['name'])<3:
            errors['registration'].append ('The Name is required and must be at least 3 characters')
            
        if len(postData['user_name'])<3:
            errors['registration'].append ('The User Name is required and must be at least 3 characters')
        else: #checks if the user_name is already in use by an existing user
            user_list = self.filter(user_name=postData['user_name'])
            if len(user_list) > 0:
                # email exists
                errors['registration'].append('The User Name you entered is already in use, please use a different email address')
        
        #verifies the password field is not empty
        if len(postData['password'])<1:
            errors['registration'].append ('The "Password" field cannot be empty')
        #checks the length of the value entered in the password field, if its less than 8 redirects
        elif len(postData['password'])<=8:
            errors['registration'].append ('The password must be at least 8 characters')
        
        #checks the confirm_password value
        if len(postData['confirm_password'])<1:
            errors['registration'].append ('The "Confirm Password" field cannot be empty')
        
        #checks that the password and confirm password lengths match
        if len(postData['password']) != len(postData['confirm_password']):
            errors['registration'].append ('The password and confirm password values must match')
        else: #if the lengths match, check if characters are an exact match
            for index in range ( len(postData['password']) ):
                if postData['password'][index] != postData['confirm_password'][index]:
                    errors['registration'].append ('The password and confirm password values must match')
                    break
        
        if len(errors['registration'])>0:
            return errors
        else:
            encrypted_pass = bcrypt.hashpw ( postData['password'].encode(), bcrypt.gensalt() )
            user = self.create(
                name = postData['name'],
                user_name = postData['user_name'],
                password = encrypted_pass
            )
            return { 'user': user }
    
    def logValidator (self, postData):
        errors = {
            'login': []
        }

        #verifies the email is n ot empty
        if len(postData['user_name'])<1:
            errors['login'].append ('The "Email" field cannot be empty')
        #verifies the password is not empty
        if len(postData['password'])<1:
            errors['login'].append ('The "Password" field cannot be empty')

        if len(errors['login'])>0:
            return errors
        else:
            try:#tries to get the user from the db
                user = User.objects.get(user_name=postData['user_name'])
            except:
                print '-----> COULD NOT FIND THE USER'
                errors['login'].append ('The email and password combination that you entered does not match our records, please try again')
                return errors
            print '-----> FOUND USER: ', user
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print '-----> THE PASSWORDS MATCH!'
                return { 'user': user }
            else:
                errors['login'].append ('The email and password combination that you entered does not match our records, please try again')
                print '-----> THE PASSWORDS DO NOT MATCH!'
                return  errors
        

class User (models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return self.name

class ItemManager (models.Manager):
    def createItem (self, postData, user_id):
        errors = []
        if len(postData['name'])<4:
            errors.append ('The Name of the item is required and must be at least 4 characters long')
        else:
            user = User.objects.get(id=user_id)
            #if the form is fine, creates the new item and adds it to the user's wish list
            newItem = self.create (
                name = postData['name'],
                creator = user
            )
            print '----> CREATED NEW ITEM:', newItem
            newItem.wished_by.add(user)
        return errors

class Item (models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey (User, related_name='created_items')
    wished_by = models.ManyToManyField (User, related_name='wished_items')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ItemManager()

    def __str__(self):
        return self.name
