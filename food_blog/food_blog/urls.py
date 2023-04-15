"""
URL configuration for food_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from recipes.views import pageNotFound, RecipeAPIDestroy, RecipeAPIUpdate, RecipeAPIList

# router = routers.DefaultRouter()
# router.register(r'recipe', RecipeViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('captcha/', include('captcha.urls')),

    # path('api/v1/', include(router.urls)),

    path('api/v1/recipe/', RecipeAPIList.as_view()),
    path('api/v1/recipe/<int:pk>/', RecipeAPIUpdate.as_view()),
    path('api/v1/recipedelete/<int:pk>/', RecipeAPIDestroy.as_view()),

    path('api/v1/drf-auth/', include('rest_framework.urls')),

    # path('api/v1/auth/', include('djoser.urls')),  # new
    # re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
