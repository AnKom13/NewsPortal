from django.shortcuts import render

# Create your views here.

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
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

    #количество записей на странице
    paginate_by = 2




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


