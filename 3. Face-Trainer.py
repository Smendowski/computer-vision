import os
# Python image library
from PIL import Image
import numpy as np
import cv2

import pickle

# base dir works on various os
DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(DIR, "images")


face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}

y_labels = []
x_train = []


for root, dirs, files in os.walk(image_dir):
	# image_dir == root -> dirs -> files
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(os.path.dirname(path)).replace(" ",
				"-").lower()
			#print(label, path)

			if not label in label_ids:
				label_ids[label] = current_id
				current_id += 1

			id_ = label_ids[label]				

			pil_image = Image.open(path).convert("L")
			size = (550, 550)
			final_image = pil_image.resize(size, Image.ANTIALIAS)
			# with gray scale conversion
			# take every pixel -> turn image into array
			image_array = np.array(pil_image, "uint8")
			#print(pil_image)
			#print(image_array,"\n")

			# Training model -> Face detector 
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5,
				minNeighbors=5)
			# Defining Region of interests - face
			for (x,y,w,h) in faces:
				roi = image_array[y:y+h, x:x+w]
				x_train.append(roi)
				y_labels.append(id_)
				#x_train.append(path) -> conversion to roi
				#y_labels.append(label) -> conversion to id

print(y_labels)
print(x_train)

with open("labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")