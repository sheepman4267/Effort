from django.urls import path
from notes import views
urlpatterns = [
    path('', views.index, name='notes_index'),
    path('<int:note>', views.index, name='note'),
    path('create', views.new_note, name='new_note'),
    path('create/<int:parent>', views.new_note, name='new_note')
    #path('<int:note>', views.note, name='display_note'),
    ]
