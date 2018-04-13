# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def redirectToMain (request):
    return redirect ('/main')

def index (request):
    if 'user_id' in request.session:
        return redirect ('/dashboard')
    return render (request, 'for_funsies/index.html')

def dashboard (request):
    #contains all items in the db
    all_items = Item.objects.all()
    print '----> ALL ITEMS:', all_items

    #contains all items on the user's wished_items
    wished_items = User.objects.get(id=request.session['user_id']).wished_items.all()
    print '----> wished ITEMS:', wished_items

    all_other_items = list(set(all_items) - set(wished_items) )

    print '-----> ITEMS NOT WISHED YET:', all_other_items

    context = {
        'all_other_items': all_other_items,
        'wished_items': wished_items
    }
    return render (request, 'for_funsies/dashboard.html', context)

def create_item_form (request):
    return render (request, 'for_funsies/create.html')

def logout(request):
    request.session.clear()
    return redirect ('/main')

def register(request):
    #if there are errors in the validator, it will return a dic with the errors
    #otherwise, it will return the newly created user object in the dictionary
    result = User.objects.regValidator(request.POST)

    if 'registration' in result:
        for tag,_list in result.iteritems():
            for error in _list:
                messages.error(request, error, extra_tags=tag)
        return redirect ('/main')
    else:
        request.session ['user_id']=result['user'].id
        request.session ['name']=User.objects.get(id=result['user'].id).name
        print '-----> REDIRECTING TO DASHBOARD'
        return redirect ('/dashboard')

def login(request):
    #this will either return a disctionary that holds the errors messages
    #or a dictionary with the object of the logged in user if there were no errors on the form validation
    result = User.objects.logValidator(request.POST)

    if 'login' in result:
        for tag,_list in result.iteritems():
            for error in _list:
                messages.error(request, error, extra_tags=tag)
        return redirect ('/main')
    else:
        request.session ['user_id']=result['user'].id
        request.session ['name']=User.objects.get(id=result['user'].id).name
        return redirect ('/dashboard')

def create_item (request):
    errors = Item.objects.createItem(request.POST, int(request.session['user_id']) )
    
    if len(errors)>0:
        for error in errors:
            messages.error(request, error)
        return redirect ('/wish_items/create')
    else:
        return redirect ('/dashboard')

def show (request, item_id):
    context = {
        'wished_by': Item.objects.get(id = item_id).wished_by.all(),
        'item_name': Item.objects.get(id = item_id).name
    }

    return render (request, 'for_funsies/show.html', context)

def delete (request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect ('/dashboard')

def remove (request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id = int(request.session ['user_id']))
    item.wished_by.remove(user)
    return redirect ('/dashboard')

def add_to_wishlist (request, item_id):
    item = Item.objects.get(id=item_id)
    user = User.objects.get(id = int(request.session ['user_id']))
    item.wished_by.add (user)

    return redirect ('/dashboard')