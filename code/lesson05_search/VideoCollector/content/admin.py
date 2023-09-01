# VideoCollector/content/admin.py
from content.models import Category, Video
from django.contrib import admin
from django.utils.html import format_html


class CategoryListFilter(admin.SimpleListFilter):
    title = "category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return [(c.name, c.name) for c in Category.objects.all()]

    def queryset(self, request, queryset):
        try:
            category = Category.objects.get(name=self.value())
        except Category.DoesNotExist:
            return queryset

        return queryset.filter(categories=category)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_filter = (CategoryListFilter,)
