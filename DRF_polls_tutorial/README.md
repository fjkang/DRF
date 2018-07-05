# 环境部署
- win10
- python 3.6
- pipenv

> 把官方的教程转换为了api版本
## 安装
1. pipenv搭建虚拟环境
```bash
pipenv install django djangorestframework
```
2. 建立项目,项目名为`mysite`,然后新建名为`polls`的app
> 注意创建项目最后的`.`
```bash
pipenv run django-admin startproject mysite .
pipenv run py manage.py startapp polls
```
3. 将`rest_framework`和`polls`加入*settings.py*的INSTALLED_APPS, 并更改时区
```python
# mysite/settings.py
...
INSTALLED_APPS = [
    ...
    'rest_framework',
    'polls',
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

## 模型创建
打开*polls/models.py*,创建`Question`和`Choice`两个模型
```python
# polls/models.py
import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

## serializer数据模型
创建*polls/serializers.py*,定义`QuestionSerializer`
```python
# polls/serializers.py
from rest_framework import serializers

from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'question_text', 'pub_date')
        model = Question
```

## ViewSet处理序列化数据
在*polls/views.py*中, 继承`ModelViewSet`暂时暴露所有model中的内容
```python
# polls/views.py
from rest_framework import viewsets

from .serializers import QuestionSerializer
from .models import Question


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
```

## api配置
1. 在根路由文件*mysite/urls.py*中,加入api的url
```python
# mysite/urls.py
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    ...
    path('admin/', admin.site.urls),
]
```
2. 创建*polls/urls.py*,并使用DefaultRouter来处理视图数据
```python
# polls/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet

router = DefaultRouter()
router.register('', QuestionViewSet, base_name='questions')

urlpatterns = router.urls
```

## 数据库迁移
```bash
pipenv run py manage.py makemigrations polls
pipenv run py manage.py migrate
```

## 通过admin后台创建polls的数据
1. 修改*polls/admin.py*文件
```python
# polls/admin.py
from django.contrib import admin

from .models import Question
from .models import Choice

admin.site.register(Question)
admin.site.register(Choice)
```
2. 创建superuser管理后台,并且启动后台
```bash
pipenv run py manage.py createsuperuser
pipenv run py manage.py runserver
```

> 到目前为止访问`http://127.0.0.1:8000/api/`,只能获取question的数据,接着我会加上choice的数据,并可以通过url进京点击查看

****

## 添加Choice在api中的显示
1. 在*polls/serializers.py*中,加上`添加ChoiceSerializer`,改成继承`HyperlinkedModelSerializer`基类,并让Question在api中显示choices
```python
# polls/serializers.py
from rest_framework import serializers

from .models import Question, Choice

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = serializers.HyperlinkedRelatedField(many=True, view_name='choice-detail', read_only=True)
    class Meta:
        fields = ('url', 'id', 'question_text', 'pub_date', 'choices')
        model = Question


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('url', 'id', 'question', 'choice_text', 'votes')
        model = Choice
```
2. 在*polls/views.py*中加入`ChoiceViewSet`
```python
# polls/views.py
from .serializers import QuestionSerializer, ChoiceSerializer
from .models import Question, Choice

...

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer 
```
3. 在*polls/urls.py*中,修改为
```python
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('choices', ChoiceViewSet)

urlpatterns = router.urls
```
