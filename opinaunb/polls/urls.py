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
    path('turmas', views.turma, name='turmas'),
    path('turmas/<str:pk>/<int:pk1>', views.turma_read, name='turma_read'),
    path('editar-avaliacao-turma/<int:pk>', views.turma_edit, name='avaliacao_turma_edit'),
    path('deletar-avaliacao-turma/<int:pk>', views.turma_delete, name='avaliacao_turma_delete'),
    path('filtro-turmas/<str:pk>/<int:pk1>', views.filtro_turma, name='filtro_turma'),

    path("denunciar/<int:pk>", views.denunciar, name="denunciar"),
    path("list_denuncias", views.lista_denuncias, name="denuncias_lista"),

    # Options Denuncia

    path("pass_denuncia/<int:pk>/<int:pk1>/<int:pk2>", views.pass_denuncia, name="pass_denuncia"),
    path("delete_denuncia/<int:pk>/<int:pk1>/<int:pk2>", views.delete_denuncia, name="delete_denuncia"),
    path("delete_user/<int:pk>/<int:pk1>/<int:pk2>", views.delete_user, name="delete_user"),
    
    # Filtros
    path('filtro-disciplina/', views.filtro_disciplina, name='filtro_disciplina'),
    path('filtro-professor/', views.filtro_professor, name='filtro_professor'),

    
]
