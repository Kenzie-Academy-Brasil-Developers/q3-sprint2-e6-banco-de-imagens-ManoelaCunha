from flask import Flask
from .kenzie import utils

app = Flask(__name__)

@app.post('/upload')
def upload():
    return utils.save_image()


@app.get('/files')
def get_files():
    return utils.list_files()
  

@app.get('/files/<extension>')
def get_files_extension(extension):
    return utils.list_files_by_extension(extension)


@app.get('/download/<file_name>')
def download(file_name):
    return utils.download_image(file_name.lower())


@app.get('/download-zip')
def download_dir_as_zip():
    return utils.download_image_zip()
