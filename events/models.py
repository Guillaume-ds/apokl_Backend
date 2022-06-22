from django.db import models
from django.contrib.postgres.fields import ArrayField
from profiles.models import Profile
from collectionsNft.models import Collection


def event_directory_path(instance, filename):
  name= instance.creator.name
  return f'photos/events/{name}/{filename}'.format(filename=filename) 

class Event(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='event',blank=True, null=True)
  collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='event',blank=True, null=True)
  addresses= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  users= ArrayField(models.CharField(max_length=10000), blank=True, default=list)
  picture2 = models.ImageField(upload_to=event_directory_path, default='', max_length=2000, blank=True)
  picture = models.ImageField(upload_to=event_directory_path, default='', max_length=2000, blank=True)
  def __str__(self):
    return self.title
  class Meta:
        ordering = ['-id']
	

  
