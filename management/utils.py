from django.core.exceptions import PermissionDenied

def check_owner_permission(request_user, instance_owner):
    if request_user != instance_owner:
        raise PermissionDenied("You do not have permission for this action.")