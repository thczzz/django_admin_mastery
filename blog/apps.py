from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


""" Overrides the default admin """
# class BlogAdminConfig(AdminConfig):
#     default_site = 'blog.admin.BlogAdminArea'


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
