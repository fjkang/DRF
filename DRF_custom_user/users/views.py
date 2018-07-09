from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.generics import ListCreateAPIView

from .forms import CustomUserCreationForm
from .models import CustomUser
from .serializers import UserSerializer

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    

class UserListView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer