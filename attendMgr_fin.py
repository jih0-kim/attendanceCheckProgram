#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import face_recognition
import cv2
import numpy as np
import datetime
import shutil
import schedule
import time

path = ".\\students\\"
path_out = ".\\output\\"

file_list = os.listdir(path)
print(file_list)

outfile_list = os.listdir(path_out)
print(outfile_list)

data = [3,4,5,9,10,12,13,14,15]
timelist = []
for i in data:
    timelist.append(datetime.datetime(2021, 4, 30, i, 18))

stuDict = {}

def initFile():
    n = 1
    fileName = ".\\output\\"+"stu"+str(n)
    fw = open(fileName+".txt", "w")
    fw.write("")
    fw.close()
    n += 1

def writeFile(dict, cnt):
    fileName = ".\\output\\"+"stu"+str(cnt[0])
    values=list(dict.values())
    keys = list(dict.keys())

    fw = open(fileName+".txt", "w")
    fw.write('params'+str(cnt[0])+ '=[')
    for k in range(len(dict.keys())):
        string = f'"seatNum":{keys[k]}, "name":"{values[k][0]}", "attend":{values[k][1]}, "attendTime":"{values[k][2]}", "runOut":{values[k][3]}, "runIn":"{values[k][4]}"'
        fw.write('{'+string+'}')
        if k != len(dict.keys())-1:
            fw.write(',')
    fw.write(']')
    fw.close()

    shutil.copyfile(fileName+'.txt', fileName+'.json')
    init_stu(file_list)
    cnt[0] += 1
    

def counting(outfile_list, cnt):
    if (len(outfile_list)-1)/2 == 0: 
        cnt = 1
    elif (len(outfile_list)-1)/2 == 1: 
        cnt = 2
    elif (len(outfile_list)-1)/2 == 2: 
        cnt = 3
    elif (len(outfile_list)-1)/2 == 3: 
        cnt = 4
    elif (len(outfile_list)-1)/2 == 4: 
        cnt = 5
    elif (len(outfile_list)-1)/2 == 5: 
        cnt = 6
    return cnt

## seatNum : [name, attendOrNot, attendTime, runOut, runIn]
def init_stu(list):
    for i in file_list:
        i = i[:-4]
        seatNum, name = i.split("_")
        stuDict[seatNum] = [name]+[0,0,0,0]

init_stu(file_list)   
print(stuDict)

known_face_encodings = []
known_face_names = []

## make face_encodings for all students
for img in file_list:
    stu_img = face_recognition.load_image_file(path+img)
    stu_face_encoding = face_recognition.face_encodings(stu_img)[0]
    known_face_encodings.append(stu_face_encoding)
    known_face_names.append(img[:-4].split("_")[1])
    

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

## Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
cnt = [1]

initFile()

schedule.every().day.at("01:50").do(writeFile,stuDict, cnt)
schedule.every().day.at("01:52").do(writeFile,stuDict, cnt)
schedule.every().day.at("01:54").do(writeFile,stuDict, cnt)
schedule.every().day.at("01:56").do(writeFile,stuDict, cnt)
schedule.every().day.at("01:58").do(writeFile,stuDict, cnt)
schedule.every().day.at("02:00").do(writeFile,stuDict, cnt)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_face_names[first_match_index]
                

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 2)
        
        
        ## Print "Hong gil dong 00:00 Attented"
        ## get attendTime ( save only "first" attending time )
        if name != "Unknown":
            now = datetime.datetime.now()
            nowTime = now.strftime('%H:%M:%S')[:]
            
            for k,v in stuDict.items():
                if v[0]==name:
                    if v[2]!=0:
                        pass
                    else:
                        v[2] = nowTime
                    m = int(now.strftime('%H:%M:%S')[3:5])
                    if 50 < m < 53:
                        if v[2] == 0:
                            pass
                        else:
                            v[3]=1
            
            display_string = nowTime[:5]+' ATTENDED'
            #cv2.putText(frame, display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
            cv2.putText(frame, display_string,(left - 30, bottom+30), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        
    # Display the resulting image
    cv2.imshow('Video', frame)
    schedule.run_pending()
    time.sleep(1)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()