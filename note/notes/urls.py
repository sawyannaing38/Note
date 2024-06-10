from django.urls import path 

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/add", views.add, name="add"),
    path("/entry/<str:category>", views.entry, name="entry"),
    path("/note/<str:category>/<str:title>", views.note, name="note"),
    path("/edit/<str:category>/<str:title>", views.edit, name="edit"),
    path("/remove/<str:category>/<str:title>", views.remove, name="remove")
]