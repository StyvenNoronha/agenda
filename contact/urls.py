from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    path('', views.index, name='index'),
    path('contato/<int:id>/', views.contact, name='contact'),
    path('contato/<int:id>/update', views.update, name='update'),
    path('<int:contact_id>/', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),

]