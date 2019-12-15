from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np 
import os
from keras.models import load_model
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC 
import tensorflow as tf
import pickle

class ExtractFeatures:
	def __init__(self):
		self.paths = []
		self.labels = []
		self.trainData = []
		self.facenet_model = load_model('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/facenet_keras.h5')
		self.input_encoder = Normalizer(norm='12')
		self.out_encoder = LabelEncoder()
		self.svm = SVC(kernel='linear')

		for root, dirs, files in os.walk('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/train'):
			for file in files: 
				self.labels.append(str(root).split('/')[-1])
				self.paths.append(os.path.join(root, file))

	def add_new_face(self, name, path):
		self.labels.extend(name)
		self.paths.extend(path)
		for i in range(0, len(self.paths)):
			image = self.extract_face(self.paths[i])
			output = self.get_faceembeddings(self.facenet_model, np.asarray(image))
			self.trainData.append(output)
		self.trainData = np.array(self.trainData)

		print("Here!")
		#Normalize all the values again
		input_encoder = Normalizer(norm='l2')
		self.trainData = input_encoder.transform(self.trainData)

		self.out_encoder.fit(self.labels)
		self.labels = self.out_encoder.transform(self.labels)

		self.svm.fit(self.trainData, self.labels)
		filename_out = '/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/encoder_model.sav'
		pickle.dump(self.out_encoder, open(filename_out, 'wb'))
		filename = '/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/finalized_model.sav'
		pickle.dump(self.svm, open(filename, 'wb'))
		print("Model Fitted&Saved")

	def predict_name(self, path):
		image = self.extract_face(path)
		output = self.get_faceembeddings(self.facenet_model, np.array(image))
		svm_models = pickle.load(open('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/finalized_model.sav', 'rb')) 
		out_encoder = pickle.load(open('/Users/kamaleshpalanisamy/Desktop/FaceRecognitionApp/backend/FaceRecoBackend/media/encoder_model.sav', 'rb'))
		output = output.reshape(1, -1)
		name = svm_models.predict(output)
		actual_name = out_encoder.inverse_transform([name])
		print(actual_name)
		return actual_name

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
			