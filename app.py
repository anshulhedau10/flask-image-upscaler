from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
import threading
from upscale_logic import imageUpscale

# base path
base_path = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# app configuration
app.static_folder = 'static'
app.config['UPLOAD_PATH'] = 'static/data'
app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg']

result_filename = 'output'
input_filename = 'input'
file_ext = ''


@app.route('/', methods=['GET', 'POST']) # render home page
def index():
    global base_path, input_filename, result_filename, file_ext
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)

        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return 'File type not supported. Please choose an image.'
            uploaded_file.save(os.path.join(base_path, app.config['UPLOAD_PATH'], str(input_filename + file_ext)))
            print('Saved file successfully')

            # call ML model
            imageUpscale(input_filename, result_filename, file_ext)

            return redirect('/download') 
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/about') # render about page
def about():
    return render_template('about.html')
    
@app.route('/download', methods=['GET']) # render download page
def download():
    # Calling maintenance function to clear images after 5 mins
    timer = threading.Timer(5*60.0, maintenance)
    timer.start()

    return render_template('download.html')

@app.route('/downloadfile', methods=['GET']) # download output
def downloadFile():
    global base_path, result_filename, file_ext
    file = os.path.join(base_path, app.config["UPLOAD_PATH"], str(result_filename + file_ext))
    try:
        return send_file(file, as_attachment=True)
    except FileNotFoundError:
        return "Timeout! Please try again :(."
    
    
#@app.after_response
def maintenance():
    # clearing out images
    for file in os.scandir('static/data'):
        try:
            os.remove(file.path)
        except:
            pass

    

    
    
if __name__ == '__main__':
    app.run()