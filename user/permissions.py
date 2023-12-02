from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
# GET : 누구나 / PUT 또는 PATCH : 해당 유저만

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # 안전한 메소드(GET)면
            return True
        return obj.user == request.user

