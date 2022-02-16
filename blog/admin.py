from django.contrib import admin
from . import models
import django.apps
from django import forms
from django.contrib import messages
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment
from django.contrib.auth.models import User, Group


class BlogAdminArea(admin.AdminSite):
    site_header = 'Blog Admin Area'
    login_template = 'blog/admin/login.html'


blog_site = BlogAdminArea(name='BlogAdmin')


""" Simple ModelAdmin """
# class PostAdmin(admin.ModelAdmin):
#     exclude = ('id', 'publish')
#
#
# blog_site.register(models.Post, PostAdmin)




""" Register all models from apps """
# models_to_reg = django.apps.apps.get_models()
#
# for model in models_to_reg:
#     try:
#         blog_site.register(models_to_reg)
#     except admin.sites.AlreadyRegistered:
#         pass
#
#
# blog_site.unregister(django.contrib.sessions.models.Session)



""" Grouping """
# class PostAdmin(admin.ModelAdmin):
#     fields = ('author', ('title', 'slug'))




""" Fieldsets """
# TEXT = 'Some text we can include'
#
#
# class PostAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Section 1', {
#             'fields': ('title', 'author',),
#             'description': '%s' % TEXT,
#         }),
#         ('Section 2', {
#             'fields': ('slug',),
#             'classes': ('collapse',),
#         }),
#     )



""" Simple Custom Admin Form """
# class PostForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PostForm, self).__init__(*args, **kwargs)
#         self.fields['title'].help_text = 'New Help Text'
#
#     class Meta:
#         model = models.Post
#         exclude = ('id', 'publish',)
#
#
# class PostFormAdmin(admin.ModelAdmin):
#     form = PostForm
#
#
# blog_site.register(models.Post, PostFormAdmin)



""" Installing Markdown Editor & adding it to the chosen fields  """


class SummerAdmin(SummernoteModelAdmin):
    summernote_fields = ('excerpt', 'content',)


# blog_site.register(models.Post, SummerAdmin)
blog_site.register(models.Category)
blog_site.register(Attachment)



""" Custom Filter & Filtering """


class EmailFilter(admin.SimpleListFilter):

    title = 'Email'
    parameter_name = 'user_email'

    def lookups(self, request, model_admin):
        return (
            ('has_email', 'has_email'),
            ('no_email', 'no_email'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'has_email':
            return queryset.exclude(user__email='')
        if self.value().lower() == 'no_email':
            return queryset.filter(user__email='')


class ProfileFilter(admin.ModelAdmin):
    list_display = ("id", "email", "created_at", "role", "is_active")
    list_filter = ("is_active", "role", "created_at", EmailFilter)


blog_site.register(models.Profile, ProfileFilter)
blog_site.register(User)
blog_site.register(Group)



""" Django Admin User Model Permission Overrides, Groups & Performing Extra Operations """


# class TestAdminPermissions(admin.ModelAdmin):
#
#     def has_add_permission(self, request):
#         profile_role = request.user.profile.role
#         if profile_role == 3 or profile_role == 4:
#             return True
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         profile_role = request.user.profile.role
#         if profile_role == 3 or profile_role == 4:
#             return True
#         return False
#
#     def has_view_permission(self, request, obj=None):
#         return True
#
#     def has_delete_permission(self, request, obj=None):
#         profile_role = request.user.profile.role
#         if profile_role == 4:
#             return obj is None or obj.pk != 1
#         return False


class TestAdminPermissions(admin.ModelAdmin):

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # def has_delete_permission(self, request, obj=None):
    #     if request.user.groups.filter(name='editors').exists():
    #         return False
    #     return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.POST.get('action') == 'delete_selected':
            messages.add_message(request, messages.ERROR, (
                "I really hope you are sure about this!"
            ))
        return True


blog_site.register(models.Post, TestAdminPermissions)
