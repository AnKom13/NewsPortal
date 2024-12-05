from django.urls import path, include
from news.views import PostList,NewsCreate, NewsList, NewsSearch, NewsDelete, NewsEdit
from news.views import ArticlesList, ArticleCreate, ArticleSearch, ArticleDelete,ArticleEdit
#from news.views import PostDetail
from news.views import detail, subscriptions

urlpatterns = [
#    path('', PostList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
# вариант вывода через адрес ex: http://127.0.0.1:8000/news/3
#    path('<int:pk>', PostDetail.as_view()),

# Вариант со списком и ссылками на элементы
# внимание на параметр name. ОН задает имя маршрута,
# т.е если потом вызвать имя с параметром, то получу полный путь
#    path('<int:pk>', detail, name='det'),

#    path('news/', PostList.as_view(), name='news'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('news/<int:pk>', detail, name='news_detail'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('article/', ArticlesList.as_view(), name='articles'),
    path('article/search/', ArticleSearch.as_view(), name='article_search'),
    path('article/<int:pk>', detail, name='article_detail'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('article/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('subscriptions/', subscriptions, name='subscriptions'),
#    # после успешного сохранения откроется детальная инфа о посте
#    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
#    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
#    path('news/search/', include('news.urls_news'), name='news_search'),
]