# 初始环境
- windos 10
- python 3.6
- pipenv

> 官方教程中,urlpatterns里使用的是`url`,我这里已转化为`path`(django2.x)

***

# 使用方法
1. 进入/DRF_snippets_tutorial

```bash
pipenv install
```

2. 启动服务

```bash
pipenv run py manage.py runserver
```

***

# 知识结构
## 基础模式
1. 将定义好的数据模型(models)序列化成Json格式

```
models-->serializers
```

2. 使用rest框架的generics基类视图将序列化数据进行views处理,其中APIViews有五种:
- ListAPIView
- CreateAPIView
- RetrieveAPIView
- UpdateAPIView
- DestroyAPIView

```
serializers-->views
```

3. 将视图处理函数与路由urls相匹配
- format_suffix_patterns:提供特定文件格式的选择(如json,api等)
```
http://127.0.0.1:8000/snippets/ <-> views.SnippetList.as_view()
```
获取所有snippet,可进行查询和添加
```
http://127.0.0.1:8000/snippets/ <-> views.SnippetDetail.as_view()
```
获取单个snippet,可进行查询,修改和删除

```
views-->urls
```

4. 权限的设置:在view的类中加入permission_classes字段
- IsAuthenticatedOrReadOnly 未登录只读
- IsOwnerOrReadOnly (自定义) 不是创建者只读
- AllowAny 允许任何人

```
permissions-->views
```

5. 加入api的根节点
- views中定义api_view
```python
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
```
- urls中加上path
```python
urlpatterns = [
    ...
    path('', views.api_root),
]
```

6. 设置分页,settings.py中加入REST_FRAMEWORK配置
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## ViewSet-->router模式
1. viewsets的使用
- ModelViewSet 默认拥有`create()`, `retrieve()`, `update()`,`partial_update()`, `destroy()` and `list()`6个处理方法
- ReadOnlyModelViewSet 拥有`list()` and `retrieve()`2个方法

2. DefaultRouter的使用
- 实例化router,注册viewset
```
router = DefaultRouter()
router.register('snippets', views.SnippetViewSet)
router.register('users', views.UserViewSet)
```
- 赋值给urlpatterns
```
urlpatterns = router.urls
```

