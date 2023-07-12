from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('minha-conta/<int:pk>/', views.minha_conta, name='minha_conta'),
    path('editar/<int:pk>/', views.editar, name='editar_conta'),
    path('delete/<int:pk>/', views.delete, name='deletar_conta'),
    path('professor', views.professor, name='professor'),
    path('professor/<int:pk>', views.professor_read, name='professor_read'),
    path('editar-avaliacao-prof/<int:pk>', views.editar_avaliacao_professor, name='avaliacao_professor_edit'),
    path('deletar-avaliacao-prof/<int:pk>/<int:pk2>', views.delete_avaliacao_prof, name='avaliacao_professor_delete'),
    path('filtro-professor/', views.filtro_professor, name='filtro_professor'),
    path('turmas', views.professor, name='turmas'),
]
