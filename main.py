import os
from flask import Flask, render_template, request, flash 
from werkzeug.utils import secure_filename
import cv2 as cv
import numpy as np
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"the operation is {operation} and the filename is {filename}")
    img =cv.imread(f"uploads/{filename}")
    
    match operation:
        
        case "gray":
            imgProcessed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "crop":
            imgProcessed = img[50:200, 200:400]
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        case "rotateL":

            def rotate(img, angle, rotPoint=None):
             (height, width) = img.shape[:2]
             if rotPoint is None:
                 rotPoint = (width // 2, height // 2)

                 rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
                 dimensions = (width, height)

                 return cv.warpAffine(img, rotMat, dimensions)

            imgProcessed = rotate(img, 90)
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "rotateR":

            def rotate(img, angle, rotPoint=None):
             (height, width) = img.shape[:2]
             if rotPoint is None:
                 rotPoint = (width // 2, height // 2)

                 rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
                 dimensions = (width, height)

                 return cv.warpAffine(img, rotMat, dimensions)

            imgProcessed = rotate(img, -90)
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename

        case "resize":
            imgProcessed =cv.resize(img, (500,500), interpolation= cv.INTER_AREA)
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "flip1":

            imgProcessed = cv.flip(img, -1)
             
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "flip2":

            imgProcessed = cv.flip(img, 1)
             
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "blur":

            imgProcessed = cv.GaussianBlur(img, (7,7), 0)
             
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
        case "rescale":
            def rescaleFrame(frame, scale=0.25):
                width = int(frame.shape[1] * scale)
                height = int(frame.shape[0] * scale)
                dimensions = (width, height)
                return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
            
            imgProcessed = rescaleFrame(img)
             
            cv.imwrite(f"static/{filename}", imgProcessed)
            return filename
        
    pass


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/edit', methods=["GET", "POST"])
def edit():
   
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        if file.filename == '':
            
            flash('No selected file', 'error')
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename, operation)
            
            flash(f"Your picture is complete and is available  <a href='/static/{filename}' target='_blank'>here</a>", 'success')
            

            return render_template("index.html")
        
    return render_template("index.html")    

app.run(debug=True)
