from django.contrib import admin
from .models import Article, Tag
from django_summernote.admin import SummernoteModelAdmin


class ArticleAdmin(SummernoteModelAdmin):
    # summernote_fields = ('title',)
	summernote_fields = '__all__'

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
