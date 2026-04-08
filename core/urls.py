from django.urls import path
from core import views
from core.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('', views.index, name='core-index'),
    path('category/', CategoryListView.as_view(), name='core-category-list' ),
    path('category/create/', CategoryCreateView.as_view(), name='core-category-create'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='core-category-detail'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='core-category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='core-category-delete'),
]