from django import template
from django.core.cache import cache

from recipes.models import Category, Recipe

register = template.Library()


@register.simple_tag(name='category')
def get_categories():
    cats = cache.get('categories')  # кэширование
    if not cats:
        cats = Category.objects.all()
        cache.set('categories', cats, 30)

    return cats




