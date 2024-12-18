from django.contrib import admin

# Register your models here.

from .models import Author, Category, Post, PostCategory, Comment


def change_content(modeladmin, request, queryset):  # все аргументы уже должны быть вам знакомы,
    # самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов,
    # которых мы выделили галочками.
    queryset.update(content='Бред')


change_content.short_description = 'Изменение контента'  # описание для более понятного представления


# в админ панеле задаётся, как будто это объект

# создаём новый класс для представления товаров в админке
class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in
                    Comment._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    list_display.append('quality')
    list_filter = ('content', 'user')  # добавляем примитивные фильтры в нашу админку
    #    search_fields = ['rate','id']
    search_fields = ['rate', 'user__username']
    actions = [change_content]  # добавляем действия в список


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
# admin.site.register(Comment)
admin.site.register(Comment, CommentAdmin)
# admin.site.unregister(Comment)
