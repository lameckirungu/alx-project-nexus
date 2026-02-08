from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		user_id = str(getattr(request.user, "id", ""))
		if hasattr(obj, "user_id"):
			return str(obj.user_id) == user_id
		if hasattr(obj, "cart"):
			return str(obj.cart.user_id) == user_id
		return False
