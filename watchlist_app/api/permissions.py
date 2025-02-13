from rest_framework import permissions

# Si es admin edita y si no solo lee
class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # si es Admin regresamos true
        # admin_permission = bool(request.user and request.user.is_staff)
        # # si es con el metodo GET o es admin
        # return request.method == 'GET' or admin_permission
        # otra manera de hacerlo
        if request.method in permissions.SAFE_METHODS:
            return True # read-only
        else:
            return bool(request.user and request.user.is_staff)



class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            # si el usuario de la review es el mismo que eta logueado puede return true
            return obj.review_user == request.user or request.user.is_staff
