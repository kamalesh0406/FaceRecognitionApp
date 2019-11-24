from django.db import models

class ImageModel(models.Model):

	name = models.CharField(max_length = 20)
	file = models.FileField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)

