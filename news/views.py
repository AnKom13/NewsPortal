from django.shortcuts import render
from django.urls import reverse_lazy

# Create your views here.

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .filters import PostsFilter
from .forms import NewsForm, ArticleForm
from .models import Post


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


def detail(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'post.html', context={'post': post})


# Классы новости
class NewsCreate(CreateView):
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
class ArticleCreate(CreateView):
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