from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2
import geocoder
from To_cal_near import neariest_hosp
from send_message import message
import keyboard
import pyfiglet

flag = False

phone_counter = 0

thres = 0.5
nms_threshold = 0.2

intro = pyfiglet.figlet_format("AcciProof")
print(intro)

driver = input("Enter the driver name: ")

classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def sound_alarm(path):

	while ALARM_ON:
		playsound.playsound(path)

def eye_aspect_ratio(eye):
	
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	
	C = dist.euclidean(eye[0], eye[3])
	
	ear = (A + B) / (2.0 * C)
	
	return ear

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=False, default="shape_predictor_68_face_landmarks.dat",
	help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="alert.mp3",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 15


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


COUNTER = 0
global ALARM_ON
ALARM_ON = False

print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)


while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=1200)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	rects = detector(gray, 0)

	classIds, confs, bbox = net.detect(frame,confThreshold=thres)
	bbox = list(bbox)
	confs = list(np.array(confs).reshape(1,-1)[0])
	confs = list(map(float,confs))

	indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)

	for rect in rects:
		
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)
		
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		
		ear = (leftEAR + rightEAR) / 2.0

        
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		
		if ear < EYE_AR_THRESH:
			COUNTER += 1
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				if not ALARM_ON:
					ALARM_ON = True
					if args["alarm"] != "":
						t = Thread(target=sound_alarm,
							args=(args["alarm"],))
						t.deamon = True
						t.start()
				
				cv2.putText(frame, "DROWSINESS ALERT!", (600, 40),
					cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)
		
		else:
			COUNTER = 0
			ALARM_ON = False

		
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
	for i in indices:
		i = i[0]
		if classNames[classIds[i][0]-1] == "cell phone":
		    phone_counter += 1
		box = bbox[i]
		x,y,w,h = box[0],box[1],box[2],box[3]
		cv2.rectangle(frame, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
		cv2.putText(frame,classNames[classIds[i][0]-1].upper(),(box[0]+10,box[1]-10),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,255,0),2)
		cv2.putText(frame, "confidence: {:.2f}".format(confs[i]), (box[0]+150,box[1]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)


		if phone_counter >= 10:
			if args["alarm"] != "":
				ALARM_ON = True
				t = Thread(target=sound_alarm,
				args=(args["alarm"],))
				t.deamon = True
				t.start()		
				phone_counter = 0	
				ALARM_ON = False

	if keyboard.is_pressed('a'):
		g = geocoder.ip('me')
		latitude, longitude = g.latlng
		data = neariest_hosp(latitude, longitude)
		hospital, contact, distance, lat, log = data
		message(driver, hospital, contact, distance, lat, log)
		flag = True

	if flag:
		cv2.putText(frame, "Nearest Hospital {}".format(hospital), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
		cv2.putText(frame, "Contact {}".format(contact), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
		cv2.putText(frame, "Distance {}Km".format(distance), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)
		cv2.putText(frame, "Messages have been sent relatives & friend are been informed", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 4)	

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()