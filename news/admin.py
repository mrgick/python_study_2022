from django.contrib import admin
from .models import News, Category
from .forms import CategoryChoiceField


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ('name', )


class CategoryInline(admin.TabularInline):
    model = Category


@admin.register(News)
class NewsModelAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'modified_date', 'created_date')

    fieldsets = ((None, {
        'fields': ('title', 'text', 'image', 'blog')
    }), ('Дополнительные опции', {
        'classes': ('collapse', ),
        'fields': ('owner', ),
    }))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog':
            return CategoryChoiceField(queryset=Category.objects.all(), label=db_field.verbose_name)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
