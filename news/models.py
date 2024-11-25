
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rate = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rate = self.post_set.aggregate(postRate=Sum('rate'))
        com_rate = self.user.comment_set.aggregate(comRate=Sum('rate'))

        self.rate = post_rate.get('postRate') * 3 + com_rate.get('comRate')
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    CHOICE = [
        ('N', 'Новость'),
        ('A', 'Статья'),
    ]

    property = models.CharField(max_length=1, choices=CHOICE, default='N')
    time_create = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    rate = models.SmallIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
#        return self.content[0:123]+'...'
#        return '{0}{1}'.format(self.content[0:123], '...')
        return f'{self.content[0:123]} ...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    rate = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
