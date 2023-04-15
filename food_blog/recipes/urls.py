from django.views.decorators.cache import cache_page

from recipes.views import about, HomeListView, ShowCategoryListView, ShowPostDetailView, AddPageCreateView, \
    RegisterUser, LoginUser, logout_user
from django.urls import path

urlpatterns = [
    # path('', cache_page(30)(HomeListView.as_view()), name='home'),
    path('', HomeListView.as_view(), name='home'),
    path('category/<int:cat_id>', ShowCategoryListView.as_view(), name='show_category'),
    path('about/', about, name='about'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('addpage/', AddPageCreateView.as_view(), name='addpage'),
    path('post/<slug:post_slug>', ShowPostDetailView.as_view(), name='show_post'),

]
