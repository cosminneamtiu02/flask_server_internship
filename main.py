import os
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    if len(files) == 6:
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Allowed image types are -> png, jpg, jpeg')
                return redirect(request.url)

        return render_template('upload.html', filenames=file_names)

    else:
        flash('There have to be 6 files.')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()

# TO RUN THE APP:
# 1.)CREATE A DIRECTORY NAMED 'static' AND A SUBDIRECTORY NAMED 'uploads'
# 2.)RUN IN TERMINAL THE COMMAND 'python main.py'
# 3.)OPEN IN BROWSER http://localhost:5000
