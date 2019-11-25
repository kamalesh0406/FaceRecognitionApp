from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np 
import os
from keras.models import load_model

class ExtractFeatures:
	def __init__(self):
		paths = []
		labels = []
		trainData = []
		for root, dirs, files in os.walk('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/train'):
			for file in files: 
				labels.append(str(root).split('/')[-1])
				paths.append(os.path.join(root, file))
		print(paths[1])
		for i in range(0, len(paths)):
			image = self.extract_face(paths[i])
			trainData.append(np.asarray(image))
		trainData = np.array(trainData)
		print(trainData.shape)
		facenet_model = load_model('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/facenet_keras.h5')
		for pixels in trainData:
			output = self.get_faceembeddings(facenet_model, pixels)
			print(output.shape)
	def add_new_face(self, name, paths):
		labels.extend(name)
		for i in range(0, len(paths)):
			image = self.extract_face(paths[i])
			trainData.append(np.asarray(image))

	def extract_face(self, filename):
		image = Image.open(filename)
		image = image.convert('RGB')
		pixels = np.asarray(image)

		detector = MTCNN()
		results = detector.detect_faces(pixels)

		x1, y1, width, height = results[0]['box']

		x1, y1 = abs(x1), abs(y1)

		x2, y2 = x1+width, y1+height

		face = pixels[y1:y2, x1:x2]

		new_image = Image.fromarray(face)
		new_image = new_image.resize((160,160))

		return new_image
	def get_faceembeddings(self, model, pixels):
		pixels = pixels.astype('float32')

		mean, std = pixels.mean(), pixels.std()
		pixels = (pixels - mean) / std 

		samples = np.expand_dims(pixels, axis=0)

		yhat = model.predict(samples)

		return yhat[0]

extract = ExtractFeatures()

			