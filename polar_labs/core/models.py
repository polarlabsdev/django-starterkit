from django.contrib.auth.models import AbstractUser


class PolarLabsUser(AbstractUser):
	pass
	# add additional fields in here

	def __str__(self):
		return self.username
