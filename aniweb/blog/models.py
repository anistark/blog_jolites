from django.db import models
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
     
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering = ['-created']
     
    def __unicode__(self):
        return u'%s' % self.title
     
    def get_absolute_url(self):
        return reverse('blog.views.post', args=[self.slug])

class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    website = models.URLField(max_length=200, null=True, blank=True)
    text = models.TextField()
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]

def add_comment(request, slug):
    """Add a new comment."""
    p = request.POST

    if p.has_key("body") and p["body"]:
        author = "Anonymous"
        if p["author"]: author = p["author"]

        comment = Comment(post=Post.objects.get(slug=slug))
        cf = CommentForm(p, instance=comment)
        cf.fields["author"].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()
    return HttpResponseRedirect(reverse("aniweb.blog.views.post", args='slug'))