from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .mlmodels.ExtractFaces import ExtractFeatures
from .models import ImageModel
from .serializers import ImageSerializer
from django.conf import settings
import os

class FileView(APIView):

	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, *args, **kwargs):
		file_locations = []
		names = request.data['name']
		files = request.data.getlist('file')
		for file in files:
			diction = {}
			diction['name']=names
			diction['file']=file
			file_serializer = ImageSerializer(data=diction)
			if file_serializer.is_valid():
				file_serializer.save()
			image_id = file_serializer.data['id']
			model = ImageModel.objects.get(id=image_id)
			file_locations.append(settings.BASE_DIR + str(model.file.url))
		print(file_locations)
		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
		# else:
		# 	return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)