from multiprocessing import context
from django.db import transaction, connection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http.response import JsonResponse
import os
import glob
import jaconv
from movie.scrape import ResponseMovieSite

from movie.forms import MovieForm, MovieFormSet, MovieMainForm, TagSelectFormSet, MovieInputForm
from movie.models import MovieFile, TagLabel, TagRelate

DIR_MOVIE_FILE_PATH = './static/moviefile/'
DIR_MOVIE_FILE_URL = '/static/moviefile/'

# Create your views here.
def index(request):

    mainForm = MovieMainForm
    movieList = MovieFormSet
    tagList = TagSelectFormSet

    if request.method == 'GET':

        mainForm = MovieMainForm(request.GET or None)
        # タグ
        try:
            tags = TagLabel.objects.all()
            tagData = []
            for tag_rec in tags:
                tagData.append({
                    'is_select' : False,
                    'tag_name' : tag_rec.tag_name,
                })
            tagList = TagSelectFormSet(initial=tagData)
        except:
            pass

        if mainForm.is_valid():
            # 初期表示
            if mainForm.cleaned_data['search_mode'] == None:
                pass
            
            # 登録
            if mainForm.cleaned_data['search_mode'] == '1':
                dirpath = DIR_MOVIE_FILE_PATH + '*.*'
                movieFileList = glob.glob(dirpath)

                movies = []
                for movieFile in movieFileList:
                    try:
                        f = MovieFile.objects.get(file_name=movieFile.replace(DIR_MOVIE_FILE_PATH,''))
                    except:
                        movies.append({
                            'file_name' : movieFile.replace(DIR_MOVIE_FILE_PATH,''),
                            'file_path' : movieFile.replace('./','/'),
                            'title' : '',
                            'actor_name' : '',
                            'order_no' : None
                        })

                movieList = MovieFormSet(initial=movies,)

            # 検索
            elif mainForm.cleaned_data['search_mode'] == '2':
                tag_check_list = []
                tagData = []
                # チェックしたタグを取得
                tagSelectFormSet = TagSelectFormSet(request.GET or None)
                if tagSelectFormSet.is_valid():
                    for tagForm in tagSelectFormSet:
                        if tagForm.cleaned_data['is_select']:
                            tag_check_list.append(tagForm.cleaned_data['tag_name'])
                        tagData.append({
                            'is_select' : tagForm.cleaned_data['is_select'],
                            'tag_name' : tagForm.cleaned_data['tag_name'],
                        })
                tagList = TagSelectFormSet(initial=tagData)

                # 検索SQL
                with connection.cursor() as search_result_cursor:
                    search_result_sql = 'select f.file_name, f.file_path, f.title, f.actor_name, f.search_str, f.movie_time'
                    search_result_sql = search_result_sql + '  from movie_moviefile as f'
                    search_result_sql = search_result_sql + ' where 1=1 '

                    # タグを検索条件に追加
                    if len(tag_check_list) > 0:
                        str_tag_labels = ''
                        search_result_sql = search_result_sql + '   and exists ( select * from movie_tagrelate as r '
                        search_result_sql = search_result_sql + '                 where r.file_name = f.file_name'
                        search_result_sql = search_result_sql + '                   and r.tag_name in ('
                        for tag_label in tag_check_list:
                            if str_tag_labels!='':
                                str_tag_labels = str_tag_labels + ','
                            str_tag_labels = str_tag_labels + "'" + tag_label + "'"
                        search_result_sql = search_result_sql + '                  ' + str_tag_labels + ')'
                        search_result_sql = search_result_sql + '             )'
                    
                    # 検索文字列を検索条件に追加
                    if mainForm.cleaned_data['search_str'] is not None and mainForm.cleaned_data['search_str']!='':
                        search_result_sql = search_result_sql + "   and f.search_str like '%" + mainForm.cleaned_data['search_str'] + "%' "
                    
                    # SQL実行
                    search_result_cursor.execute(search_result_sql)
                    search_result = search_result_cursor.fetchall()
                    movies = []

                    # フェッチ
                    for data in search_result:
                        movies.append({
                            'file_name' : data[0],
                            'file_path' : data[1].replace('./','/'),
                            'title' : data[2],
                            'actor_name' : data[3],
                            'movie_time' : data[5],
                            'order_no' : None,
                        })

                movieList = MovieFormSet(initial=movies,)

        
        context = {
            'mainForm' : mainForm,
            'movieList' : movieList,
            'tagList' : tagList,
        }

        return render(request, 'movie/index.html', context)
    
    if request.method == 'POST':

        context = {
            'mainForm' : mainForm,
            'movieList' : movieList,
            'tagList' : tagList,
        }

        return render(request, 'movie/index.html', context)

# 登録画面へ遷移
def edit(request,file):
    if request.method == 'GET':

        # movieFile = get_object_or_404(MovieFile,file_name=file)

        movieInputForm = None;
        tagList = TagSelectFormSet

        try:
            movieFile = MovieFile.objects.get(file_name=file)
            movieInputForm = MovieInputForm(instance=movieFile)

        except:
            movieData = {
                'file_name' : file,
                'file_path' : DIR_MOVIE_FILE_PATH + file,
                'title' : '',
                'actor_name' : '',
                'movie_time' : 360,
                'order_no' : '',
            }
            movieInputForm = MovieInputForm(movieData)

        try:
            tags = TagLabel.objects.all()
            tagData = []
            for tag_rec in tags:
                tagExist = TagRelate.objects.filter(file_name=file,tag_name=tag_rec.tag_name)
                isTagRelate = False
                if tagExist.count()!=0:
                    isTagRelate = True
                
                tagData.append({
                    'is_select' : isTagRelate,
                    'tag_name' : tag_rec.tag_name,
                })
            tagList = TagSelectFormSet(initial=tagData)
        except:
            pass


        context = {
            'movieForm' : movieInputForm,
            'tagList' : tagList,
            'movieUrl' : DIR_MOVIE_FILE_URL + file
        }

    return render(request, 'movie/edit.html', context)

# 登録処理
def input(request):
    if request.method == 'POST':
        
        with transaction.atomic():
            movieForm = MovieInputForm(request.POST)
            if movieForm.is_valid():

                try:
                    movieFile = MovieFile.objects.get(file_name=movieForm.cleaned_data['file_name'])
                    movieFile.file_path = movieForm.cleaned_data['file_path']
                    movieFile.title      = movieForm.cleaned_data['title']
                    movieFile.actor_name = movieForm.cleaned_data['actor_name']
                    movieFile.search_str = ''
                    movieFile.movie_time = movieForm.cleaned_data['movie_time']
                except:
                    movieFile = MovieFile(
                        file_name  = movieForm.cleaned_data['file_name'],
                        file_path  = movieForm.cleaned_data['file_path'],
                        title      = movieForm.cleaned_data['title'],
                        actor_name = movieForm.cleaned_data['actor_name'],
                        search_str = Fn.search_str(movieForm.cleaned_data['title'] + movieForm.cleaned_data['actor_name']),
                        movie_time = movieForm.cleaned_data['movie_time'],
                    )
                movieFile.save()

            tagFormSet = TagSelectFormSet(request.POST)
            if tagFormSet.is_valid():
                tagRetateDel = TagRelate.objects.filter(file_name=movieForm.cleaned_data['file_name'])
                tagRetateDel.delete()
                for tagForm in tagFormSet:
                    if tagForm.cleaned_data['is_select']:
                        tagRetate = TagRelate(
                            file_name = movieForm.cleaned_data['file_name'],
                            tag_name = tagForm.cleaned_data['tag_name'],
                        )
                        tagRetate.save()

        return redirect('/movie/?search_mode=1')
    

# 動画情報を取得
def movieinfo(request,file):
    if request.method == 'GET':
        movieInfo = ResponseMovieSite(file).info()
        print(movieInfo)
        return JsonResponse(movieInfo, safe=False)

# タグ登録
def tag(request,process,tag_label_name):
    if request.method == 'GET':
        tagLabel = None
        try:
            tagLabel = TagLabel.objects.filter(tag_name=tag_label_name)
        except:
            pass

        if process=='add':
            if tagLabel==None or tagLabel.count()==0:
                tagLabel = TagLabel(tag_name=tag_label_name)
                tagLabel.save()
            else:
                pass

        tagLabelData = []
        for tag_rec in TagLabel.objects.all():
            tagLabelData.append({
                'is_select' : False,
                'tag_name' : tag_rec.tag_name,
            })
        return HttpResponse(TagSelectFormSet(initial=tagLabelData))

# 動画再生
def start(request):
    if request.method == 'GET':
        movieList = MovieFormSet(request.GET or None)
        movies = []
        movieCnt = 0
        if movieList.is_valid():
            for movieFile in movieList:
                print('loop:' + movieFile.cleaned_data['order_no'])
                if movieFile.cleaned_data['order_no'] is not None and movieFile.cleaned_data['order_no']!='':
                    # movies.append(movieFile)
                    movies.insert(int(movieFile.cleaned_data['order_no'])-1,movieFile)
                    movieCnt = movieCnt + 1
        context = {
            'movies' : movies,
            'total' : movieCnt,
        }

        return render(request, 'movie/start.html', context)

# 動画再生テストページ
def index2(request):
    return render(request, 'movie/index2.html')

# 検索用文字列変換
class Fn:
    def search_str(val):
        # 英字は全て小文字
        convert_lower = val.lower().replace(' ','').replace(' ','')
        # print(convert_lower)

        # 半角を全角
        convert_han2zen = jaconv.h2z(convert_lower, kana=False, digit=True, ascii=True)
        convert_han2zen = jaconv.hankaku2zenkaku(convert_han2zen)
        # print(convert_han2zen)

        # カタカナをひらがな
        convert_hi = jaconv.kata2hira(convert_han2zen)
        # print(convert_hi)

        return convert_hi