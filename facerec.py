import cv2, os, sys
import numpy as np
from PIL import Image

def face_finder(image_path):
    
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    Team = {1:'Dhoni',2:'Ashwin',3:'Rohit',4:'Umesh',5:'Rahane',6:'Shikar',7:'Raina',8:'Jadeja',9:'Virat'}

    recognizer = cv2.createLBPHFaceRecognizer()

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        images = []
        labels = []
        for image_path in image_paths:
            image_pil = Image.open(image_path).convert('L')
            image = np.array(image_pil, 'uint8')
            nbr = int(os.path.split(image_path)[1].split(".")[0].replace("output", ""))
            images.append(image)
            labels.append(nbr)
        
        return images, labels

    path = './myfaces'

    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()

    recognizer.train(images, np.array(labels))

    oplabels = []
    identified = []

    predict_image_pil = Image.open(image_path).convert('L')
    predict_image = np.array(predict_image_pil, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        img_patch = predict_image[y:y+h,x:x+w]
        gray_image = cv2.resize(img_patch,(32, 32), interpolation = cv2.INTER_CUBIC)
        nbr_predicted, conf = recognizer.predict(gray_image)
        oplabels.append(nbr_predicted);
      
    for l in oplabels:
        identified.append(Team[l])
 		
    return identified
    
    

