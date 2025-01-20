import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.utils.translation import gettext as _

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page

from django.views.decorators.csrf import csrf_protect

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from .models import *


# Create your views here.

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView

#from django.utils.translation import (activate, get_supported_language_variant)

#, LANGUAGE_SESSION_KEY)

from .filters import PostsFilter
from .forms import NewsForm, ArticleForm
from .models import Post
from .models import Subscriber, Category

#==========
from django.views import View
from django.http.response import HttpResponse  # импортируем респонс для проверки текста

from django.utils import timezone
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


@cache_page(60*5)
@login_required
def detail(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'post.html', context={'post': post})


from .tasks import hello
#import time
# class IndexView(View):
#     def get(self,request):
# #        time.sleep(10)
# #        hello.delay(10)
#         hello.delay()
#         return HttpResponse('Za_ra_bo_ta_lo!!!')

# class IndexView(TemplateView):
#   template_name = 'post_list.html'
#   def get_context_data(self, **kwargs):
#     context = super(IndexView, self).get_context_data(**kwargs)
#     hello()
#     return context

class IndexView(View):
    def get(self, request):
        # .  Translators: This message appears on the home page only
        string = _('Hello World')
        context = {
            'string': string,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }
        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

class IndexViewOld1(View):
    def get(self, request):
        string = _('Hello World')
        context = {
            'string': string
        }
        return HttpResponse(render(request,'index.html', context))


class IndexViewOld(View):
    def get(self, request):
#        hello()
#        hello.delay()
#        hello.apply_async()
        string = _('Hello World')
        str2 = _('Check')
        return HttpResponse(string)
class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post'

    # По ТЗ надо выводить список новостей, а не всех постов
    # Для этого реализован этот фильтр. Если его убрать, тогда queryset вернет все записи
    queryset = Post.objects.all().filter(property='N')

    # количество записей на странице
    paginate_by = 5

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# Использовал этот класс, пока не переделал через функцию detail
# class PostDetail(DetailView):
# Модель всё та же, но мы хотим получать информацию по отдельному товару
#    model = Post
# Используем другой шаблон — post.html
#    template_name = 'post.html'
# Название объекта, в котором будет выбранный пользователем продукт. Далее это название будет использоваться в html
# если эта переменная не указана, тогда в html вместо {% for p in post %} надо {% for p in object_list %}
#    context_object_name = 'post'


# Классы новости
class NewsCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'post'
    queryset = Post.objects.all().filter(property='N')
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs


class NewsSearch(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'news_search.html'
    context_object_name = 'post'
    queryset = Post.objects.all().filter(property='N')
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


# классы Статей
class ArticleCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


class ArticlesList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'articles_list.html'
    context_object_name = 'post'
    queryset = Post.objects.all().filter(property='A')
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs


#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['filterset'] = self.filterset
#        return context


class ArticleSearch(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'article_search.html'
    context_object_name = 'post'
    queryset = Post.objects.all().filter(property='A')
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles')

class ArticleEdit(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

#API
class PostAPIViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()

   serializer_class = PostSerializer
   filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
   filterset_fields = ["property"]

class CommentAPIViewset(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer
   permission_classes = [permissions.AllowAny]


class CategoryAPIViewset(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer
