from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.redirectToMain),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.create_item_form),
    url(r'^wish_items/create_item$', views.create_item),
    url(r'^wish_items/(?P<item_id>\d+)$', views.show),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),
    url(r'^add_to_wishlist/(?P<item_id>\d+)$', views.add_to_wishlist)
]