from django.db import models

# Create your models here.

class MovieFile(models.Model):
    file_name = models.CharField(
        verbose_name='ファイル名',
        max_length=256,
        blank=False,
        default=' ',
    )

    file_path = models.CharField(
        verbose_name='ファイルの場所',
        max_length=256,
        blank=True,
        default=' ',
    )
    
    title = models.CharField(
        verbose_name='タイトル',
        max_length=256,
        blank=True,
        default=' ',
    )
    
    actor_name = models.CharField(
        verbose_name='主演',
        max_length=256,
        blank=True,
        default=' ',
    )

    search_str = models.CharField(
        verbose_name='検索文字列',
        max_length=256,
        blank=True,
        default=' ',
    )

    movie_time = models.IntegerField(
        verbose_name='再生時間',
        blank=True,
        default=360,
    )

class TagLabel(models.Model):
    tag_name = models.CharField(
        verbose_name='タグ',
        max_length=256,
        blank=True,
        default=' ',
    )
    
class TagRelate(models.Model):
    file_name = models.CharField(
        verbose_name='ファイル名',
        max_length=256,
        blank=True,
        default=' ',
    )

    tag_name = models.CharField(
        verbose_name='タグ',
        max_length=256,
        blank=True,
        default=' ',
    )
    

