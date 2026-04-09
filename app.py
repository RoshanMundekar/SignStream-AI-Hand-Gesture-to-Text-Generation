from flask import *
import pymysql
import tflearn
from tflearn.layers.conv import conv_2d,max_pool_2d
from tflearn.layers.core import input_data,dropout,fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
import cv2
import imutils


app = Flask(__name__)

def dbConnection():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="root", database="dbroadpotholes",charset='utf8')
        return connection
    except:
        print("Something went wrong in database Connection")

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")

con=dbConnection()
cursor=con.cursor()

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploaded_img/'
app.secret_key = 'random string'

##########################################################################################################
#                                           Register
##########################################################################################################
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        # print("hii register")
        email = request.form['Email']
        mobileno = request.form['mobileno']
        password = request.form['pass1']
        username = request.form['Name']

        print(email,password,username)

        try: 
            con = dbConnection()
            cursor = con.cursor()
            sql1 = "INSERT INTO tblregister (uname, email, password, mobile) VALUES (%s, %s, %s, %s)"
            val1 = (username, email, password, mobileno)
            cursor.execute(sql1, val1)
            print("query 1 submitted")
            con.commit()

            FinalMsg = "Congrats! Your account registerd successfully!"
        except:
            con.rollback()
            msg = "Database Error occured"
            print(msg)
            return render_template("login.html", error=msg)
        finally:
            dbClose()
        return render_template("login.html",FinalMsg=FinalMsg)
    return render_template("register.html")
##########################################################################################################
#                                               Login
##########################################################################################################
@app.route("/", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password'] 

        print(email,password)

        con = dbConnection()
        cursor = con.cursor()
        result_count = cursor.execute('SELECT * FROM tblregister WHERE email = %s AND password = %s', (email, password))
        result = cursor.fetchone()
        print("result")
        print(result)
        if result_count>0:
            print("len of result")
            session['uname'] = result[1]
            session['userid'] = result[0]
            return redirect(url_for('root'))
        else:
            result_count = cursor.execute("Select * FROM tbladmin WHERE email=%s AND password=%s", (email, password))
            result = cursor.fetchone()
            if result_count == 1:
                session['uname'] = result[1]
                session['userid'] = result[0]
                return redirect(url_for("adminindex"))
            else:
                return render_template('login.html')
    return render_template('login.html')
##########################################################################################################
#                                       Product Description
##########################################################################################################
@app.route("/single", methods = ['POST', 'GET'])
def productDescription():
    
    return render_template('services.html')
##########################################################################################################
#                                               about
##########################################################################################################
@app.route("/about", methods = ['POST', 'GET'])
def about():
    username=session.get('uname')
    return render_template('about.html')
##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/contact", methods = ['POST', 'GET'])
def contact():
    username=session.get('uname')
    return render_template('contact.html',firstName=username)
##########################################################################################################
#                                               contact
##########################################################################################################
@app.route("/logout", methods = ['POST', 'GET'])
def logout():
    session.pop('uname',None)
    session.pop('userid',None)
    return redirect(url_for('login'))
#########################################################################################################
#                                       Home page
##########################################################################################################
@app.route("/root")
def root():
    if 'uname' in session:

        return render_template('index.html')
########################################### UPLOAD IMAGE  ###################################################################
# global variables
bg = None
camera = None
capture_requested = False
predicted_text = "None"
predicted_confidence = "0%"

create_gesture_name = ""
images_captured = 0

def init_camera():
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)
    return camera

def release_camera():
    global camera
    if camera is not None and camera.isOpened():
        camera.release()
    camera = None

def resizeImage(imageName):
    basewidth = 100
    img = Image.open(imageName)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.LANCZOS)
    img.save(imageName)

# Model defined
convnet=input_data(shape=[None,89,100,1],name='input')
convnet=conv_2d(convnet,32,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,64,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,128,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,256,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,256,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,128,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=conv_2d(convnet,64,2,activation='relu')
convnet=max_pool_2d(convnet,2)
convnet=fully_connected(convnet,1000,activation='relu')
convnet=dropout(convnet,0.75)
convnet=fully_connected(convnet,3,activation='softmax')
convnet=regression(convnet,optimizer='adam',learning_rate=0.001,loss='categorical_crossentropy',name='regression')

model=tflearn.DNN(convnet,tensorboard_verbose=0)
model.load("Major Project/TrainedModel/GestureRecogModel.tfl")

def getPredictedClass():
    image = cv2.imread('Temp.png')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    prediction = model.predict([gray_image.reshape(89, 100, 1)])
    return np.argmax(prediction), (np.amax(prediction) / (prediction[0][0] + prediction[0][1] + prediction[0][2]))

def generate_frames_detect():
    global capture_requested, predicted_text, predicted_confidence, bg
    cam = init_camera()
    bg = None
    num_frames = 0
    aWeight = 0.5
    top, right, bottom, left = 10, 350, 225, 590
    
    while True:
        success, frame = cam.read()
        if not success:
            break
            
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        
        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        if num_frames < 30:
            if bg is None:
                bg = gray.copy().astype("float")
            else:
                cv2.accumulateWeighted(gray, bg, aWeight)
            cv2.putText(clone, "Calibrating Background: Wait...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        else:
            diff = cv2.absdiff(bg.astype("uint8"), gray)
            thresholded = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            cnts, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(cnts) != 0:
                segmented = max(cnts, key=cv2.contourArea)
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                
                if capture_requested:
                    cv2.imwrite('Temp.png', thresholded)
                    resizeImage('Temp.png')
                    cl, conf = getPredictedClass()
                    if cl == 0:
                        predicted_text = "You are awsome"
                    elif cl == 1:
                        predicted_text = "Fist"
                    elif cl == 2:
                        predicted_text = "Hello user"
                    predicted_confidence = str(round(conf * 100, 2)) + "%"
                    capture_requested = False

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(clone, f"Prediction: {predicted_text} ({predicted_confidence})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        num_frames += 1
        ret, buffer = cv2.imencode('.jpg', clone)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames_create():
    global create_gesture_name, capture_requested, images_captured, bg
    cam = init_camera()
    bg = None
    num_frames = 0
    aWeight = 0.5
    top, right, bottom, left = 10, 350, 225, 590
    import os
    
    while True:
        success, frame = cam.read()
        if not success:
            break
            
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        
        roi = frame[top:bottom, right:left]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        if num_frames < 30:
            if bg is None:
                bg = gray.copy().astype("float")
            else:
                cv2.accumulateWeighted(gray, bg, aWeight)
            cv2.putText(clone, "Calibrating Background: Wait...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        else:
            diff = cv2.absdiff(bg.astype("uint8"), gray)
            thresholded = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            cnts, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(cnts) != 0:
                segmented = max(cnts, key=cv2.contourArea)
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                
                if capture_requested:
                    save_dir = "Major Project/Dataset/" + create_gesture_name + "Images"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    cv2.imwrite(f"{save_dir}/{create_gesture_name}_{images_captured}.png", thresholded)
                    images_captured += 1
                    capture_requested = False

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(clone, f"Captured: {images_captured} - Name: {create_gesture_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        num_frames += 1
        ret, buffer = cv2.imencode('.jpg', clone)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed_detect')
def video_feed_detect():
    return Response(generate_frames_detect(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_create')
def video_feed_create():
    return Response(generate_frames_create(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/stop_camera', methods=['POST'])
def api_stop_camera():
    release_camera()
    return jsonify({"status": "success"})

@app.route('/api/trigger_predict', methods=['POST'])
def api_trigger_predict():
    global capture_requested
    capture_requested = True
    return jsonify({"status": "success"})

@app.route('/api/get_prediction', methods=['GET'])
def api_get_prediction():
    global predicted_text, predicted_confidence
    return jsonify({"prediction": predicted_text, "confidence": predicted_confidence})

@app.route('/api/start_create', methods=['POST'])
def api_start_create():
    global create_gesture_name, images_captured, capture_requested
    data = request.json
    create_gesture_name = data.get('signame', 'unknown')
    images_captured = 0
    capture_requested = False
    return jsonify({"status": "success"})

@app.route('/api/trigger_capture', methods=['POST'])
def api_trigger_capture():
    global capture_requested
    capture_requested = True
    return jsonify({"status": "success"})

@app.route('/api/get_capture_status', methods=['GET'])
def api_get_capture_status():
    global images_captured
    return jsonify({"images_captured": images_captured})

@app.route("/history", methods=['POST', 'GET'])
def userhistory():
    return render_template('userDetails.html')

if __name__=='__main__':
    app.run('0.0.0.0')