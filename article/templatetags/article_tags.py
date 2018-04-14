from ..models import Article,Tag
from django import template

from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
	"""
	used in html like:
	{% get_recent_articles %}
	"""
	return Article.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def get_update_articles():
        """
        used in html like:
        {% get_recent_articles %}
        """
        return Article.objects.filter(updating=1).order_by('-created_time')


@register.simple_tag
def archives():
    return Article.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_tags():
	return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
