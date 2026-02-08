from dataclasses import dataclass

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


@dataclass
class JwtUser:
	id: str

	@property
	def is_authenticated(self) -> bool:
		return True


class StatelessJWTAuthentication(JWTAuthentication):
	def get_user(self, validated_token):
		user_id = validated_token.get("user_id") or validated_token.get("sub")
		if not user_id:
			raise AuthenticationFailed("Token missing user_id")
		return JwtUser(str(user_id))
