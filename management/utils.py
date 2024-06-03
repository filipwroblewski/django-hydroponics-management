from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

def check_owner_permission(request_user: User, instance_owner: User) -> None:
    if request_user != instance_owner:
        raise PermissionDenied("You do not have permission for this action.")