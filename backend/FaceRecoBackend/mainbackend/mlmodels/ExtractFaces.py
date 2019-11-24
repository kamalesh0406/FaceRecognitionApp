from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np 



class ExtractFeatures:
	def extract_face(filename):
		image = Image.open(filename)
		image = image.convert('RGB')
		pixels = np.asarray(image)
		print(pixels.shape)

		detector = MTCNN()
		results = detector.detect_faces(pixels)

		x1, y1, width, height = results[0]['box']

		x1, y1 = abs(x1), abs(y1)

		x2, y2 = x1+width, y1+height

		face = pixels[y1:y2, x1:x2]

		new_image = Image.fromarray(face)
		new_image = new_image.resize((160,160))

		return new_image
			