from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.contact, name='contact'),
    path('search/', views.search, name='search'),

]