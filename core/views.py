from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Category


@login_required
def index(request):
    return render(request, 'core/index.html')


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'core/category/list.html'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'core/category/detail.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name = 'core/category/create.html'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'core/category/update.html'


class CategoryDeleteView(DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'core/category/delete.html'
