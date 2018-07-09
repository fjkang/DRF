# 部署环境
- win10
- python 3.6
- pipenv

> 这是一个继承官方user模型,自定义users的app例子

## 安装

```bash
pipenv install django
pipenv run django-admin startproject djauth .
pipenv run py .\manage.py startapp users
```

创建django虚拟环境,创建djauth项目,创建users应用
* 注意,对于我们需要新建的users,不要先使用`migrate`命令!

## 继承AbstractUser
继承用户模型,需要4个步骤
1. 更新`settings.py`
- 在`INSTALL_APPS`中加入`users`和增加`AUTH_USER_MODEL`配置

```python
INSTALLED_APPS = [
    ...
    'users',
]
...
AUTH_USER_MODEL = 'users.CustomUser'
```

2. 在`users/model.py`中创建一个`CustomUser`模型

```python
# users/model.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 以下可加入想要的字段
    # age = models.IntegerField(default=0)

    def __str__(self):
        return self.username # 这里是AbstractUser里面定义好的
```

这里先写好框架,继续下一步

3. 创造新的`UserCreation`和`UserChangeForm`
首先创建`users/forms.py`文件,写入:

```python
# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
```

这样就能最大程度的继承官方User模型里的表单功能

4. 更新`users/admin.py`,让`CustomUser`与默认的Admin耦合

```python
# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email',]

admin.site.register(CustomUser, CustomUserAdmin)
```

最后,运行`makemigrations`和`migrate`命令

```bash
pipenv run py .\manage.py makemigrations users
pipenv run py .\manage.py migrate
```

## 创建超级管理员

```bash
pipenv run py .\manage.py createsuperuser
```

## 视图/网址/模板

1. 在`settings.py`中设置

```python
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
]
# 登陆和登出重定向到home
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

接着创建模板html,新建`templates`和`templates/registration`目录
- 基础模板

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{% block title %}Django CustomUser{% endblock %}</title>
</head>
<body>
  <main>
    {% block content %}
    {% endblock %}
  </main>
</body>
</html>
```

- 主页模板

```html
<!-- templates/home.html -->
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
{% if user.is_authenticated %}
  Hi {{ user.username }}!
  <p><a href="{% url 'logout' %}">logout</a></p>
{% else %}
  <p>You are not logged in</p>
  <a href="{% url 'login' %}">login</a> |
  <a href="{% url 'signup' %}">signup</a>
{% endif %}
{% endblock %}
```

- 登陆模板

```html
<!-- templates/registration/login.html -->
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
{% endblock %}
```

- 注册模板

```html
<!-- templates/signup.html -->
{% extends 'base.html' %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<h2>Sign up</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>
{% endblock %}
```

2. `urls.py`的配置
- `djauth/urls.py`

```python
# djauth/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
```

- `user/urls.py`

```python
# user/urls.py
from django.urls import path

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]
```

3. `views`的配置
在`users/views.py`中写一个处理注册的`SignUp`方法

```python
# users/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
```

# 总结
利用以上的步骤,当我想增加一个`age`字段时,只需在
1. `models.py`中的`CustomUser`加入字段如:

```python
class CustomUser(AbstractUser):
    # 以下可加入想要的字段
    age = models.IntegerField(default=0)
```

2. `forms.py`中的`fields`加入:
```python
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        ...
        fields = ('username', 'email', 'age') # 加上age
```

3. `admin.py`中的`CustomUserAdmin`加入:
```python
class CustomUserAdmin(UserAdmin):
    ...
    list_display = ['username', 'email', 'age', 'is_active', 'is_staff', 'is_superuser'] # 这里加入age
    # 重写fieldsets,可以在管理员修改自定义数据,我这里是在Personal info新增了age
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
```

OK,更多详细信息可以查看[官方文档](https://docs.djangoproject.com/en/2.0/topics/auth/customizing/)


_ _ _

# 拓展DRF

1. 安装`djangorestframework`和`django-rest-auth`,并创建`api`应用

```bash
pipenv install djangorestframework
pipenv install django-rest-auth
pipenv run py .\manage.py startapp api
```

2. 在`settings.py`中加入:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',

    'api',
    'users',
]
```

3. 设置`api`的路由:
- 在`djauth/urls.py`的配置

```python
# djauth/urls.py
urlpatterns = [
    ...
    path('api/v1/', include('api.urls')),
]
```

- 在`api/urls.py`的配置

```python
# api/urls.py
from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
]
```

4. 创建users的`serializers.py`文件,写入:

```python
# users/serializers.py
from rest_framework import serializers

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age')
```

5. 创建users的`views.py`的api处理方法:

```python
# users/views.py
...
from rest_framework.generics import ListCreateAPIView
...
from .models import CustomUser
from .serializers import UserSerializer

...

class UserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
```

6. 最后创建users的`urls.py`写入:

```python
# users/urls.py
from .views import SignUp, UserListView

urlpatterns = [
    ...
    path('', UserListView.as_view()),
]
```

接着,就可以通过
- http://127.0.0.1:8000/api/v1/users/
- http://127.0.0.1:8000/api/v1/rest-auth/login/
- http://127.0.0.1:8000/api/v1/rest-auth/logout/
查看到对应api的接口了

# django的allauth
1. 首先安装`django-allauth`

```bash
pipenv install django-allauth
```

2. 修改`settings.py`的内容:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    ...
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
```

3. 进行数据库的更新:

```bash
pipenv run py .\manage.py migrate
```

4. 最后在`api/urls.py`中加上注册的路由

```python
# api/urls.py
urlpatterns = [
    ...
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
```

这样,通过 http://127.0.0.1:8000/api/v1/rest-auth的api 进行
- 登陆: http://127.0.0.1:8000/api/v1/rest-auth/login
- 注册: http://127.0.0.1:8000/api/v1/rest-auth/registration
- 登出: http://127.0.0.1:8000/api/v1/rest-auth/logout