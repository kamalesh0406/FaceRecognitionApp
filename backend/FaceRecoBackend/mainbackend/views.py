from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .mlmodels.ExtractFaces import ExtractFeatures
from .models import ImageModel
from .serializers import ImageSerializer
from django.conf import settings
import os

class Signup(APIView):

	parser_classes = (MultiPartParser, FormParser)
	def post(self, request, *args, **kwargs):
		file_locations = []
		names = []
		files = request.data.getlist('file')
		for file in files:
			diction = {}
			diction['name']= request.data['name']
			diction['file']=file
			file_serializer = ImageSerializer(data=diction)
			if file_serializer.is_valid():
				file_serializer.save()
			image_id = file_serializer.data['id']
			model = ImageModel.objects.get(id=image_id)
			names.append(diction['name'])
			file_locations.append(settings.BASE_DIR + str(model.file.url))
		print(file_locations)
		extract_faces = ExtractFeatures()
		extract_faces.add_new_face(names, file_locations)
		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
		# else:
		# 	return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

	parser_classes = (MultiPartParser, FormParser)

	def extract(self, path):
		

		return super(Login, self).extract(path)
	def post(self, request, *args, **kwargs):
		file_serializer = ImageSerializer(data=request.data)

		if file_serializer.is_valid():
			file_serializer.save()
		image_id = file_serializer.data['id']	
		model = ImageModel.objects.get(id=image_id)

		extract_faces = ExtractFeatures()
		extract_faces.predict_name(settings.BASE_DIR + str(model.file.url))
		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
