from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify
from tinymce import HTMLField

# Create your models here.

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username
class Category(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title
class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField('Content')
    slug = models.SlugField(default=slugify(title))
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    category = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        slug = slugify(self.title)
        return reverse('post-detail', kwargs={
            'slug':slug
        })
    