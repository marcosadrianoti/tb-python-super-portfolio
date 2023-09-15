from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite acesso a admin sempre
        if request.user.is_superuser:
            return True
        # Permite acesso se o objeto pertence a quem faz a requisição
        return obj.user == request.user
