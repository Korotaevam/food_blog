from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from recipes.forms import AddPostForm, RegisterUserForm, LoginUserForm
from recipes.models import Recipe, Category
from recipes.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from recipes.serializers import RecipeSerializer
from recipes.utils import DataMixin


class HomeListView(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'posts'

    # title = 'Home'  # присваевается в TitleMixin
    # paginate_by = 2 # см DataMixin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_dict = self.get_user_context(title='Home')
        return dict(list(context.items()) + list(mixin_dict.items()))

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True).select_related(
            'cat')  # select_related уменьшает колво sql запросов


class ShowCategoryListView(DataMixin, ListView):
    model = Recipe
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = Category.objects.get(pk=self.kwargs['cat_id'])
        mixin_dict = self.get_user_context(title='Категория -' + str(cat_selected.name), cat_selected=cat_selected)
        return dict(list(context.items()) + list(mixin_dict.items()))

    def get_queryset(self):
        return Recipe.objects.filter(cat_id=self.kwargs['cat_id']).select_related(
            'cat')  # select_related уменьшает колво sql запросов


def about(request):
    return render(request, 'recipes/about.html')


class ShowPostDetailView(DataMixin, DetailView):
    model = Recipe
    template_name = 'recipes/show_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_dict = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(mixin_dict.items()))


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not Found</h1>')


class AddPageCreateView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    # title = 'ADD Recipe'  # присваевается в DataMixin
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_dict = self.get_user_context(title='ADD Recipe')
        return dict(list(context.items()) + list(mixin_dict.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'recipes/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_dict = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(mixin_dict.items()))

    def form_valid(self, form):  # вызывается при успешной регистации
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'recipes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_dict = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(mixin_dict.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


# class RecipeViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
#
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer


class RecipeAPIList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # pagination_class = RecipeAPIListPagination


class RecipeAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, IsOwnerOrReadOnly)


class RecipeAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrReadOnly,)
