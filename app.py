import os
import PIL
import extcolors
from flask import Flask, render_template, request
app = Flask(__name__)

UPLOAD_DIRECTORY = './static/images/'


def get_color(name):
    img = PIL.Image.open(name)
    colors, pixel_count = extcolors.extract_from_image(img)
    rbgvalues = [color[0] for color in colors if isinstance(color, tuple)]
    return rbgvalues


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'No file uploaded', 400

    image = request.files['image']
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    if image.filename.split('.')[-1].lower() not in allowed_extensions:
        return 'Invalid file extension', 400
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    tempfile = f"temp.{image.filename.split('.')[-1].lower()}"
    fileloc = os.path.join(UPLOAD_DIRECTORY, tempfile)

    image.save(fileloc)
    colors = get_color(fileloc)
    return render_template('index.html', filename=fileloc, values=colors)


if __name__ == '__main__':
    app.run()
