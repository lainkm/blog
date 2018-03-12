from django.shortcuts import render, get_object_or_404
from .models import Article, Tag
from comments.forms import CommentForm
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.generic import ListView, DetailView

# chinese
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# search
from django.db.models import Q 

# def index(requset):
# 	# article_list = Article.objects.all().order_by('-created_time')
# 	article_list = Article.objects.all() # set in meta using desc order
# 	context = {
# 		'article_list': article_list
# 	}
# 	return render(requset, 'article/index.html', context)


class IndexView(ListView):
	model = Article
	template_name = 'article/index.html'
	context_object_name = 'article_list'
	paginate_by = 4



# def detail(requset, pk):
# 	article = get_object_or_404(Article, pk=pk)
# 	article.increase_read_times()
# 	article.body = markdown.markdown(article.body,
# 					extensions=[
# 					'markdown.extensions.extra',
# 					'markdown.extensions.codehilite',
# 					'markdown.extensions.toc',
# 					])
	
# 	form = CommentForm()
# 	comment_list = article.comment_set.all()
# 	context = {
# 		'article': article,
# 		'form': form,
# 		'comment_list': comment_list
# 	}
# 	return render(requset, 'article/detail.html', context)

class ArticleDetailView(DetailView):
	model = Article
	template_name = 'article/detail.html'
	context_object_name = 'article'

	def get(self, request, *args, **kwargs):
		# get 方法的调用看成是 detail 视图函数的调用
		# get 方法返回的是一个 HttpResponse 实例
		# 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
		# 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
		response = super(ArticleDetailView, self).get(request, *args, **kwargs)

		# 将文章阅读量 +1
		# 注意 self.object 的值就是被访问的文章 post
		self.object.increase_read_times()

		# 视图必须返回一个 HttpResponse 对象
		return response

	def get_object(self, queryset=None):
		# 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
		article = super(ArticleDetailView, self).get_object(queryset=None)
		# article.body = markdown.markdown(article.body,
		# 								extensions=[
		# 								'markdown.extensions.extra',
		# 								'markdown.extensions.codehilite',
		# 								'markdown.extensions.toc',
		# 								])
		md = markdown.Markdown(extensions=[
								'markdown.extensions.extra',
								'markdown.extensions.codehilite',
								'markdown.extensions.toc',
								TocExtension(slugify=slugify),
								])
		article.body = md.convert(article.body)
		article.toc = md.toc
		return article

	def get_context_data(self, **kwargs):
		# 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
		# 还要把评论表单、post 下的评论列表传递给模板。
		context = super(ArticleDetailView, self).get_context_data(**kwargs)
		form = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
		    'form': form,
		    'comment_list': comment_list
		}) # python dict method
		return context



# def archives(request, year, month):
#     article_list = Article.objects.filter(created_time__year=year,
# 											created_time__month=month
# 											).order_by('-created_time')
#     context = {
# 		'article_list': article_list
# 	}
#     return render(request, 'article/index.html', context)

class ArchivesView(ListView):
	"""
	覆写了父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据。
	为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为。
	首先是需要根据从 URL 中捕获的分类 id（也就是 pk）获取分类，
	这和 category 视图函数中的过程是一样的。不过注意一点的是，在类视图中，
	从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
	非命名组参数值保存在实例的 args 属性（是一个列表）里。
	所以我们使了 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值。
	然后我们调用父类的 get_queryset 方法获得全部文章列表，
	紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。
	"""
	model = Article
	template_name = 'article/archives.html'
	context_object_name = 'article_list'

	def get_queryset(self):
		year = self.kwargs.get('year')
		month = self.kwargs.get('month')
		return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
																created_time__month=month)
class TagView(ListView):
	model = Article
	template_name = 'article/tags.html'
	context_object_name = 'article_list'

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
	q = request.GET.get('q')
	error_msg = ''

	if not q:
		error_msg = "请输入关键词"
		return render(request, 'article/Index.html', {'error_msg':error_msg})

	article_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return render(request, 'article/index.html', {'error_msg':error_msg, 'article_list':article_list})

def page_not_found(request):
    return render(request, '404.html')

def page_errors(request):
    return render(request, '500.html')