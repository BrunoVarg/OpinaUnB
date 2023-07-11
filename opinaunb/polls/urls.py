from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('minha-conta/<int:pk>/', views.minha_conta, name='minha_conta'),
    path('editar/<int:pk>/', views.editar, name='editar_conta'),
    path('delete/<int:pk>/', views.delete, name='deletar_conta')
]
