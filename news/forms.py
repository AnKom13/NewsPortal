from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__' #все поля кроме id
        # лучше все перечислять, чтобы не вывести поля которые не нужны
        fields = ['heading', 'content', 'author', 'category', 'property', ]


    def clean(self):
        cleaned_data = super().clean()
        heading = cleaned_data.get("heading")
        content = self.cleaned_data.get("content")
        if heading == 'XXX':
            raise ValidationError({
                "heading": "Такой теме здесь не место"
            })

        if heading == content :
#        if len(heading) == 3:
            print(content)
            raise ValidationError(
                "Тема не равна содержанию"
                )


        return cleaned_data

    def clean_heading(self):
#        cleaned_data = super().clean()
        heading = self.cleaned_data.get("heading")

#        if heading == content :

        if len(heading) == 5:
            raise ValidationError(
                "Тема  длина"
            )
        return heading

class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['property'].initial = 'N'

    class Meta:
        model = Post
        fields = ['heading', 'content', 'author', 'category', 'property', ]

    #пример доп. валидатора на поле
    def clean_property(self):
        pr = self.cleaned_data.get("property")
        if pr != 'N':
            raise ValidationError("Это не статья, а новость")
        return 'N'

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['property'].initial = 'A'

    class Meta:
        model = Post
        fields = ['heading', 'content', 'author', 'category', 'property']

    #пример доп. валидатора на поле
    def clean_property(self):
        pr = self.cleaned_data.get("property")
        if pr != 'A':
            raise ValidationError("Это не новость, а статья")
        return 'A'


'''         
from news.forms import PostForm
f = PostForm({'heading': 'Shell', 'property': 'N', 'content': 'Запуск через Shell', 'author': 'Curt', })
f = PostForm({'heading': 'Shell', 'property': 'N', 'content': 'Запуск через Shell', 'author': 4, 'rate': 0, 'category': [1,2], })
f = PostForm({'heading': 'XXX', 'property': 'N', 'content': 'Запуск через Shell', 'author': 4, 'rate': 0, 'category': [1,2], })
f = PostForm({'heading': 'XX1', 'property': 'N', 'content': 'XX1', 'author': 4, 'rate': 0, 'category': [1,2], })
f.is_valid()
False
'''
