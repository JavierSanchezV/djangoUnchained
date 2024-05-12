from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/query", views.search, name="search"),
    path("new/entry", views.new, name="new"),
    path("edit/<str:entryTitle>", views.edit, name="edit"),
    path("random/entry", views.randomEntry, name="randomEntry"),
    path("<str:entryTitle>", views.entry, name="entry"),
    
]
