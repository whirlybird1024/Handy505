# USAGE
# python pokedex.py

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import pickle
import json
import time
import cv2
import os

import cfg

# define the configuration dictionary
CONFIG = {
	# define the paths to the CNN
	"model_path": os.path.sep.join(["assets", "pokedex.model"]),

	# define the set of class labels (these were derived from the
	# label binarizer from the previous post)
	"labels": [0]
}

# initialize the current frame from the video stream, a boolean used
# to indicated if the screen was clicked, a frame counter, and the
# predicted class label
frame = None
clicked = False
counter = 0
predLabel = None
scanning = False
vs = None

class scan():
        def __init__(self, screen):
                self.screen = screen
                global vs

                i = 0
                while i <= 150:
                        CONFIG["labels"].Append(str(format((i+1), '03')))
                        i += 1
                
                # load the trained convolutional neural network and pokemon database
                print("[INFO] loading pokedex model...")
                model = load_model(CONFIG["model_path"])
                #db = json.loads(open(CONFIG["db_path"]).read())

                # initialize the video stream and allow the camera sensor to warm up
                print("[INFO] starting video stream...")
                # vs = VideoStream(src=0).start()
                vs = VideoStream(usePiCamera=True).start()
                time.sleep(2.0)

                

        def inputHandler(self, action):
                # grab a reference to the global variables
                global frame, clicked, predLabel, scanning,vs
                screen = self.screen

                # check to see if the left mouse button was clicked, and if so,
                # perform the classification on the current frame
                if(action == "A" and scanning):
                        predLabel = classify(preprocess(frame))
                        clicked = True
                elif(action == "A" and not scanning):
                        addMon(predLabel, True)
                        soundFile = 'sound/dexterEntries/'+predLabel+".wav"
                        
                        if(path.exists(soundFile)):
                            pygame.mixer.music.load(soundFile)
                            pygame.mixer.music.set_volume(cfg.VOLUME)
                            pygame.mixer.music.play()
                elif(action == "B" and scanning):
                        cfg.CURRENT_MODE = 0
                        cv2.destroyAllWindows()
                        vs.stop()
                #elif(action == "B" and not scanning):
                         

        def scanning(self):
                # loop over the frames from the video stream
                global frame, clicked, predLabel, scanning,vs
                screen = self.screen

                while True:
                        # if the window was clicked "freeze" the frame and increment
                        # the total number of frames the stream has been frozen for
                        if clicked and count < CONFIG["display_for"]:
                                count += 1

                        else:
                                # grab the frame from the threaded video stream and resize
                                # it to have a maximum width of 260 pixels
                                frame = vs.read()
                                frame = imutils.resize(frame, width=480, inter=cv2.INTER_NEAREST)
                                (fgH, fgW) = frame.shape[:2]

                                # reset our frozen count, clicked flag, and predicted class
                                # label
                                count = 0
                                clicked = False
                                predLabel = None
                                screen.blit(frame, (0,0))

                        # if the predicted class label is not None, then draw the Pokemon
                        # stats on the Pokedex
                        if predLabel is not None:
                                #predLabel is the dex#
                                mon = pygame.image.load("pics/sugimori/"+predLabel+".png")
                                mon = pygame.transform.scale(mon, (350,350))
                                screen.blit(mon, (50,50))
                                addMon(predLabel, True)
                                
        def addMon(num, caught):
            lines = {}
            
            with open('csv/dexOwnerList.csv') as csvfile:
                ownData = csv.DictReader(csvfile)
                for row in ownData:
                    for column, value in row.iteritems():
                        lines.setdefault(column, []).append(value)

            holder = {}
            with open('csv/dexHolder.csv') as csvfile:
                holderData = csv.DictReader(csvfile)
                for row in holderData:
                    holder = row

            print lines['caught'][num-1]
            if(caught and lines['caught'][num-1] == '0'):
                    print "caught!"
                    lines['caught'][num-1] = 1
                    
                    holder['Own'] = (int(holder['Own']) + 1)
                    holder['caught'] = (int(holder['caught']) + 1)

                    if(lines['seen'][num-1] == '0'):
                        print 'seen!'
                        lines['seen'][num-1] = 1
                        holder['seen'] = (int(holder['seen']) + 1)
                    print holder['Own']
                    
            elif(not caught and lines['seen'][num-1] == '0'):
                    lines['seen'][num-1] = 1
                    holder['seen'] = (int(holder['seen']) + 1)
            print holder['name']
            headers = ['name','class','intro','seen','caught','Own']        
            with open('csv/dexHolder.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerow(holder)

            headers = ['species_id','name','pokedex_number','seen','caught']
            with open('csv/dexOwnerList.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for data in lines['species_id']:
                    #print lines
                    #print lines[data]
                    #print data
                    temp = {}
                    i=0
                    while i<len(headers):
                        #print data[i]
                        temp[headers[i]] = lines[headers[i]][int(data)-1]
                        #print headers[i]
                        #print temp[headers[i]]
                        i+=1
                    #print temp
                                        

def preprocess(image):
	# preprocess the image
	image = cv2.resize(image, (96, 96))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# return the pre-processed image
	return image

def classify(image):
	# classify the input image
	proba = model.predict(image)[0]

	# return the class with the largest predicted probability
	return CONFIG["labels"][np.argmax(proba)]




