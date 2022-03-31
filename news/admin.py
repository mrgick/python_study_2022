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
    readonly_fields = ('modified_date', 'created_date')
    fieldsets = ((None, {
        'fields': ('title', 'text', 'image', 'blog')
    }), ('Дополнительные сведения', {
        'classes': ('collapse', ),
        'fields': ('owner', 'modified_date', 'created_date'),
    }))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog':
            return CategoryChoiceField(queryset=Category.objects.all(),
                                       label=db_field.verbose_name)
        elif db_field.name == 'owner':
            user = request.user
            news_id = request.resolver_match.kwargs.get('object_id')
            if not news_id:
                kwargs['initial'] = user.id

            if not user.is_superuser:
                kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def is_owner_or_superuser(self, request, obj) -> bool:
        """
        Check if user is owner
        """
        if obj == None:
            return True
        elif request.user == obj.owner or request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None) -> bool:
        if self.is_owner_or_superuser(request, obj):
            return super().has_change_permission(request)
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        if self.is_owner_or_superuser(request, obj):
            return super().has_add_permission(request)
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        if self.is_owner_or_superuser(request, obj):
            return super().has_add_permission(request)
        return False

    def has_view_permission(self, request, obj=None) -> bool:
        if self.is_owner_or_superuser(request, obj):
            return super().has_view_permission(request)
        return False

    def get_search_results(self, request, queryset, search_term):

        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        user = request.user
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)
        return queryset, may_have_duplicates
