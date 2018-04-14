from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import markdown
from django.utils.html import strip_tags


class Tag(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Article(models.Model):
	title = models.CharField(max_length=120)
	body = models.TextField()
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()
	read_times = models.PositiveIntegerField(default=0)
	summry = models.CharField(max_length=400, blank=True)
	tags = models.ManyToManyField(Tag, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	updating = models.IntegerField(choices=((0, "No"),(1, "YES")), default=0)	

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		"""
		in html ,using 
			<a href="{{ article.get_absolute_url }}">{{ article.title }}</a>
			to replace:

		<a href="{% url 'article:detail' article.id %}">{{ article.title }}</a>
		"""
		return reverse('article:detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created_time']

	def increase_read_times(self):
		self.read_times += 1
		self.save(update_fields=['read_times'])

	def save(self, *args, **kwargs):
		if not self.summry:
			md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
			self.summry = strip_tags(md.convert(self.body))[:200]
		super(Article, self).save(*args, **kwargs)
