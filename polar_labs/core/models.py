from django.contrib.auth.models import AbstractUser


class CoreUser(AbstractUser):
	pass
	# add additional fields in here

	def __str__(self):
		return self.username
