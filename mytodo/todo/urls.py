from django.urls import path
from django.contrib.auth.views import LogoutView
from .import views

from .views import CustomLoginView, RegisterView

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path("", views.ListListView.as_view(), name="index"),
    path("list/<int:list_id>/",views.ItemListView.as_view(), name="list"),
    path("list/add/", views.ListCreate.as_view(), name="list-add"),
    path("list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"),
    path("list/<int:list_id>/item/add/",views.ItemCreate.as_view(),name="item-add"),
    path("list/<int:list_id>/item/<int:pk>/",views.ItemUpdate.as_view(),name="item-update"),
    path("list/<int:list_id>/item/<int:pk>/delete/",views.ItemDelete.as_view(),name="item-delete"),

]
