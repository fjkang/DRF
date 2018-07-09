from django.urls import path

from .views import SignUp, UserListView

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('', UserListView.as_view()),
]