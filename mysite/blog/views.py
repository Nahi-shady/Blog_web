from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail


from dotenv import load_dotenv
load_dotenv()
import os

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 2

def post_detail(request, year,month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                                                            slug=post,
                                                            publish__year=year,
                                                            publish__month=month,
                                                            publish__day=day)
    
    return render(request, 'blog/post/detail.html', {'post': post})



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{form["name"]} recommended you to read {post.title}'
            message = f'Read {post.title} at {post_url} \n \n'\
                      f'{form["name"]}\'s comment: {form["comment"]} \n'\
                        f'sender\'s email: {form["email"]}'
            send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), [form['to']])
            sent = True
    
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                     'form': form,
                                                    'sent': sent})
