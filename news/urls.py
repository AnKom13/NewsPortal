from django.urls import path, include
from news.views import PostList
#from news.views import PostDetail
from news.views import detail

urlpatterns = [
    path('', PostList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
# вариант вывода через адрес ex: http://127.0.0.1:8000/news/3
#    path('<int:pk>', PostDetail.as_view()),

# Вариант со списком и ссылками на элементы
# внимание на параметр name. ОН задает имя маршрута,
# т.е если потом вызвать имя с параметром, то получу полный путь
    path('<int:pk>', detail, name='det'),
]