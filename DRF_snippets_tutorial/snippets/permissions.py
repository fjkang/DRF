from rest_framework import permissions

class IsOnwerOrReadOnly(permissions.BasePermission):
    """
    自定义权限:只允许拥有者对对象有编辑的权限
    """
    def has_object_permission(self, request, view, obj):
        # 对任意request都有读的权限,所以使用SAFE_METHODS(包含GET,HEAD和OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 只允许拥有者编辑
        return obj.owner == request.user
