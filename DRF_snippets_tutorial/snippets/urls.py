from django.urls import path
from rest_framework.routers import DefaultRouter
from snippets import views

# 创建一个router并用它来注册viewsets
router = DefaultRouter()
router.register('snippets', views.SnippetViewSet)
router.register('users', views.UserViewSet)

urlpatterns = router.urls