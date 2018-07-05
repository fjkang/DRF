from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import renderers

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOnwerOrReadOnly


class SnippetViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet自动包含了'list', 'create', 'retrieve', 'update'和'destroy'功能
    然后,还需要加上自定义的'highlight'功能
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOnwerOrReadOnly)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    viewsets自动提供了'list'和'retrieve'的功能
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
