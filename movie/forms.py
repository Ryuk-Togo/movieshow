from cProfile import label
from email.policy import default
from django import forms
from django.forms import formsets
from django.db import models
from movie.models import MovieFile, TagLabel, TagRelate

SEARCH_MODE = (
    ('1','登録'),
    ('2','検索'),
)

class MovieMainForm(forms.Form):

    search_mode = forms.ChoiceField(
        label='',
        widget=forms.RadioSelect,
        choices=SEARCH_MODE,
        # initial=1,
    )

    search_str = forms.CharField(
        label='検索',
        required=False,
    )

class MovieInputForm(forms.ModelForm):

    class Meta:
    
        model = MovieFile
        fields = ('file_name','file_path','title','actor_name','movie_time')
        widgets = {
            'file_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'file_path': forms.TextInput(attrs={'readonly': 'readonly'}),
            'title': forms.TextInput(),
            'actor_name': forms.TextInput(),
            'movie_time': forms.TextInput(),
        }

class MovieForm(forms.ModelForm):

    order_no = forms.IntegerField(
        label='順序',
        required=False,
    )

    class Meta:

        model = MovieFile
        fields = ('file_name','file_path','title','actor_name','movie_time')
        widgets = {
            'file_name': forms.HiddenInput(),
            'file_path': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'readonly': 'readonly'}),
            'actor_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'movie_time': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    

MovieFormSet = formsets.formset_factory(form=MovieForm, extra=0,)


class MovieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_no'].widget.attrs['class'] = 'order-no-class'

    order_no = forms.CharField(
        label='順序',
        required=False,
    )

    class Meta:

        model = MovieFile
        fields = ('file_name','file_path','title','actor_name','movie_time')
        widgets = {
            'file_name': forms.HiddenInput(),
            'file_path': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'readonly': 'readonly'}),
            'actor_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'movie_time': forms.HiddenInput(),
        }
    

MovieFormSet = formsets.formset_factory(form=MovieForm, extra=0,)

class TagSelectForm(forms.Form):
    is_select = forms.BooleanField(
        label='',
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'tag-check-class'}
        )
    )

    tag_name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'tag-name-class'}),
    )

TagSelectFormSet = formsets.formset_factory(form=TagSelectForm, extra=0,)

class MovieTagForm(forms.Form):
    
    class Meta:
        model = TagRelate
        fields = ('file_name','tag_name')
        widgets = {
            'file_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'tag_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class MovieInputForm(forms.ModelForm):
    
    class Meta:
        model = MovieFile
        fields = ('file_name','file_path','title','actor_name','movie_time')
        widgets = {
            'file_name': forms.TextInput(),
            'file_path': forms.TextInput(attrs={'readonly': 'readonly'}),
            'title': forms.TextInput(),
            'actor_name': forms.TextInput(),
            'movie_time': forms.NumberInput(),
        }
