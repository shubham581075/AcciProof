# AcciProof - The Accident Alert Tool

# Problem Description :-

      * The main agenda behind this project is to minimize the increase in the amount of
      accidents taking place on roadways in our day to day life due to the distraction faced by
      the driver.

      * Many such distractions include - drowsiness, overdrinking, using cell phones , etc.

      * Due to late arrival of ambulances at the accident spot also leads to loss of people's lives.

      * In the remote areas where we don’t have nearby hospitals info due to which many people
      lose their lives.

      * If the driver's condition is very critical then there is no available tool so that someone can
      inform his/her family or friends.
      
      
# Proposed Solution :- 

      ● To solve the above problem we have tried to develop a system which we
      have named as “AcciProof”.
      
      ● In this system there will be two parts where one part will deal with an
      accident-prevention( object detection) system which will alert the driver if
      the driver is feeling sleepy or using the phone while driving.
      
      ● And the other part will serve as life saving which will be a notification
      system that will send alerts to the nearest hospital and driver’s relatives if
      any accident happens.


# Software Tools :- 

     ● Development Tools: VS Code
    
     ● Programming Language used: Python
     
     ● Technologies and API used: OpenCV-Python, Geopy, JSON
     
     ● Python Libraries used: pyfiglet, imutils, dlib, scipy, numpy, argparse,
     serial, geocoder, geopy.
     
     
# Working :-

  # First part of the project :

     ● We have implemented an object detection model using coco dataset ,
     which was trained using Single Shot Detector (SSD) technique.
     
     ● Single Shot detector takes only one shot to detect multiple objects present in
     an image using a multibox.
     
     ● High speed and accuracy of SSD using relatively low resolution images is
     attributed due to following reasons :
     
          1. Eliminates bounding box proposals like the ones used in RCNN’s
          2. Includes a progressively decreasing convolutional filter for
          predicting object categories and offsets in bounding box locations.
          
     ● We have developed our model (net) using trained weights and network
     configuration with the help of Deep Neural Networks.
     
     ● It can detect 91 objects with a quite good accuracy score.
     
     ● It draws a rectangle around the object with the class name of the object on
     the top left corner of the frame of video , beside which lies the confidence
     score with which the object was predicted by our trained model.
     
     ● We have used dlib library to detect faces and facial landmarks .
     
     ● To detect facial landmarks we have used a dataset which contains different
     facial landmark images to accurately detect our facial features.
     
     ● With the help of this we calculate the aspect ratio of left and right eyes and
     then conclude if it's open or not.
     
     ● If eyes are closed then beep sound will be produced in background to alert
     the driver.
     
   # The second part of this project:
   
     ● We have developed an alert system which will be activated if any accident
     happens, it will send the text messages to the nearest hospital, driver’s
     relatives and friends containing the driver’s location, route to his/her
     location and his health history( blood pressure, sugar etc).
     
     ● We will be using the Geocoder API for finding the driver’s location where
     the accident has happened. Geocoder API finds the location using the IP
     address of the person.
     
     ● We have maintained a database of hospitals which will be providing this
     service and will select the hospital which will be having the shortest distance
     from the driver’s location.
     
     ● We have used the Geopy API for calculating the distance between hospitals
     and the drivers. It calculates the distance between two locations using the
     coordinates of the locations.
     
     ● We have used Twilio API for sending messages to nearby hospitals and
     driver’s relatives.

# How to run ?

     * First you should have all the mentioned libraries installed and if some libraries
     are still missing then you can go to Pypi.org to install them.

     * You should have an account on TWILIO so that you can use there messaging services.

     * You have to register your friend and relatives phone numbers in driver_info.json
     if you are the driver.

     * We have just added few hospitals of Delhi NCR and Mumbai in hub_coords.json therefore
     you can add hospital according to your location.
     
     * drowziness.py is the final file that to be executed to get the video frame it will 
     alert you if you're feeling drowsy or using phone , you can inform relatives , friends
     and nearest hospital about the accident by just pressing the key 'a' from the keyboard. 
     
     * To show the working we have invoked the message feature by pressing the key 'a' from
     the keyword but in real life it will be invoke using some hardware in the vehicle
     eg. something like an IOT device.
