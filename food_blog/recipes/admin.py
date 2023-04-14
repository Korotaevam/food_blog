from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import Recipe, Category


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    fields = (
        'title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>") # mark_safe не экранирует теги
        else:
            return "Нет фото"

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
