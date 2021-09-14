from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="new_page"),
    path("<str:name>/edit", views.edit, name="edit"),
    path("<str:name>", views.title, name="title")
]
