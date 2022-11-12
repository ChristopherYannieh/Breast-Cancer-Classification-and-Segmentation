from flask import Flask, request, render_template, redirect, flash
from main import getPrediction
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np

UPLOAD_FOLDER = 'static/images/'

app = Flask(__name__, static_folder='static', template_folder='website')  

app.secret_key = 'secret key'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file.')
            return redirect(request.url)
        file = request.files['file']   
        if file.filename == '':
            flash('No file selected for uploading.')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predicted_class, img, prediction_mask = getPrediction(filename)
            flash(predicted_class)

            actual_image = Image.fromarray((img * 255).astype(np.uint8))
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}_256x256.png')
            actual_image.save(img_filename)
            
            mask = Image.fromarray((prediction_mask[:,:,0] * 255).astype(np.uint8))
            mask_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_mask.png")
            mask.save(mask_filename)

            flash(img_filename)
            flash(mask_filename)
            
            return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)