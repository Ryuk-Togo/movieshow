from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "movie"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('index2', views.index2, name='index2'),
    path('edit/<str:file>', views.edit, name='edit'),
    # path('input', views.input, name='input'),
    url(r'^input/$', views.input, name='input'),
    # url(r'^(?P<url>\w+)/$', views.index, name='index'),
    # path('<str:url>', views.index, name='index'),
    path('tag/<str:process>/<str:tag_label_name>', views.tag, name='tag'),
    path('start', views.start, name='start'),
    path('movieinfo/<str:file>', views.movieinfo, name='movieinfo'),
]