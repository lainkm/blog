from django.shortcuts import render, get_object_or_404, redirect
from article.models import Article

from .models import Comment
from .forms import CommentForm


def post_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        print('hah')

        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.article = article

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(article)

        else:
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = article.comment_set.all()
            context = {'article': article,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'article/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(article)
