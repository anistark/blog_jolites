# Create your views here.
from django.shortcuts import render, render_to_response, get_object_or_404
from blog.models import Post, Comment, CommentForm
from django.core.context_processors import csrf

def index(request):
    # get the blog posts that are published
    posts = Post.objects.filter(published=True)
    # now return the rendered template
    return render(request, 'blog/index.html', {'posts': posts})
     
def post(request, slug):
    # get the Post object
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response('blog/post.html', d)
    # now return the rendered template
    # return render(request, 'blog/post.html', {'post': post})

def add_comment(request, pk):
    """Single post with comments and a comment form."""
    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response('blog/post.html', d)