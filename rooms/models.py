from django.db import models
from django.contrib.auth.models import User
from nfts.models import NFT


class Room(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	stars = models.IntegerField()
	creator = models.ForeignKey(User, on_delete=models.CASCADE)

