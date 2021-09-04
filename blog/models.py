from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.functional import cached_property
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache

from datetime import datetime
import markdown
from markdown.extensions.toc import TocExtension


# Create your models here.
class Category(models.Model):
    name = models.CharField('分类名', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')

    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    excerpt = models.CharField('摘要', max_length=200, blank=True)

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    toc = md.toc
    return {"content": content, "toc": toc}


def change_post_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("post_updated_at", datetime.utcnow())


def change_category_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("category_updated_at", datetime.utcnow())


def change_tag_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set("tag_updated_at", datetime.utcnow())


post_save.connect(receiver=change_post_updated_at, sender=Post)
post_delete.connect(receiver=change_post_updated_at, sender=Post)

post_save.connect(receiver=change_category_updated_at, sender=Category)
post_delete.connect(receiver=change_category_updated_at, sender=Category)

post_save.connect(receiver=change_tag_updated_at, sender=Tag)
post_delete.connect(receiver=change_tag_updated_at, sender=Tag)
