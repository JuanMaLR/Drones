import cv2 as opencv

path_face_xml = './Resources/haarcascade_frontalface_default.xml'
path_eye_xml = './Resources/haarcascade_eye.xml'

def is_there_a_face():
    face_cascade = opencv.CascadeClassifier(path_face_xml)
    try:
        i = 1
        while (i < 10):
            i += 1
            img = opencv.imread(r'/Users/LeonRodriguez/anaconda3/lib/python3.7/site-packages/pyparrot/images/visionStream.jpg')
            if (img is not None):
                gray = opencv.cvtColor(img, 0)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) >= 1:
                    return 'Face found'
        return 'No face'
    except:
        print("Error in face")
        return 'No face'

def follow(bebop):
    face_cascade = opencv.CascadeClassifier(path_face_xml)
    eye_cascade = opencv.CascadeClassifier(path_eye_xml)
    try:
        img = opencv.imread(r'/Users/LeonRodriguez/anaconda3/lib/python3.7/site-packages/pyparrot/images/visionStream.jpg')
        if (img is not None):
            gray = opencv.cvtColor(img, 0)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                w_min_size = 60
                w_max_size = 85
                print("W: ", w)
                #Estoy lejos
                if w < w_min_size:
                    print("forward")
                    if w < 45:
                        bebop.fly_direct(0, 35, 0, 0, 2)
                    else:
                        bebop.fly_direct(0, 35, 0, 0, 1)
                    bebop.ask_for_state_update()
                    bebop.smart_sleep(1)
                elif w > w_max_size:
                    print("backwards")
                    bebop.fly_direct(0, -20, 0, 0, 1)
                    bebop.ask_for_state_update()
                    bebop.smart_sleep(1)
                #Estoy no centrado Izq der
                elif (x + (w / 2)) > (856 / 2 + 60):
                    print("right")
                    bebop.fly_direct(30, 0, 0, 0, 1)
                    bebop.ask_for_state_update()
                    bebop.smart_sleep(1)
                elif (x + (w / 2)) < (856 / 2 - 60):
                    print("lft")
                    bebop.fly_direct(-20, 0, 0, 0, 1)
                    bebop.ask_for_state_update()
                    bebop.smart_sleep(1)
                else:
                    print("search Eyes")
                    j = 0
                    blink = 0
                    roi_gray = gray[y : y + h, x : x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    if len(eyes) == 0:
                        #Land
                        bebop.safe_land(10)
                        print("Blink")
                        bebopVision.close_video()
                        bebop.disconnect()
                    else:
                        print("No blink found")
    except:
        print("Error in follow")
