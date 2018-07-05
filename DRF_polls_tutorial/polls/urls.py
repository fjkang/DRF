from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('choices', ChoiceViewSet)

urlpatterns = router.urls