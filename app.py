from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask import render_template
from flask_wtf.csrf import CSRFProtect
import os
import script


SECRET_KEY = os.urandom(32)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'upload/')

app = Flask(__name__, template_folder='templates', static_folder='frontend')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

csrf = CSRFProtect(app)
csrf.init_app(app)


@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/resize")
def resize():
    return render_template('resize.html')


@app.route("/thanks")
def thanks():
    return render_template('thanks.html')

@app.route("/about-us")
def about():
    return render_template('about_us.html')


@app.route('/load-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    
        if 'file' not in request.files:
            print("not file_name")
            return jsonify(result='error', data="Choose file!")
        file = request.files.getlist('file')[0]
        if file.filename == '':
            print("file name is empty")
            return jsonify(result='error', data="File name is empty!")
        else:
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            new_image = None
            if request.form.get('alghoritm') == '1':
                new_image = script.nn_interpolate(filename, int(request.form.get('scale')))
            if request.form.get('alghoritm') == '2':
                new_image = script.bicubic(filename, int(request.form.get('scale')))
            if request.form.get('alghoritm') == '3': 
                new_image = script.bilinear(filename, int(request.form.get('scale')))
            
            os.remove(app.config['UPLOAD_FOLDER'] + filename)
            return  jsonify({'result': 'success', 'image': new_image})

                
    return jsonify(result='error', data="error")


if __name__=='__main__':
    app.run(debug=True)
