import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from . import FILES_DIRECTORY
from . import ALLOWED_EXTENSIONS
from . import MAX_CONTENT_LENGTH

app = Flask(__name__)

def save_image():
    file_image = request.files.get('file')
    file_name = secure_filename(file_image.filename)

    size_max = int(MAX_CONTENT_LENGTH)*1024*1024
    size_file = request.content_length
 
    if size_file > size_max:
        return {"message": "Arquivo maior que 1MB!"}, 413

    for file_extension in ALLOWED_EXTENSIONS:
        if file_extension in file_name.lower():
            file_path = os.path.join(f'{FILES_DIRECTORY}/{file_extension}', file_name)
    
            if not os.path.exists(file_path):
                file_image.save(f'{FILES_DIRECTORY}/{file_extension}/{file_name}')
                return {"message": "Upload realizado com sucesso!"}, 201
        
            return {"message": "Nome de arquivo já existente!"}, 409
 
    return {"message": "Extensão de arquivo não suportada!"}, 415


def list_files():
    list_files = [', '.join(os.listdir(f'{FILES_DIRECTORY}/{extension}')) for extension in ALLOWED_EXTENSIONS]

    return jsonify(list_files), 200


def list_files_by_extension(extension):
    for allowed_extension in ALLOWED_EXTENSIONS:

        if allowed_extension == extension:
            list_files_by_extension = os.listdir(f'{FILES_DIRECTORY}/{extension}')
            return jsonify(list_files_by_extension), 200

    return {"message": "Formato de arquivo invalido!"}, 404


def download_image(file_name):
    for file_extension in ALLOWED_EXTENSIONS:
        if file_extension in file_name:
            file_path = os.path.join(f'{FILES_DIRECTORY}/{file_extension}')

            return send_from_directory(
                directory=f'../{file_path}',
                path=file_name,
                as_attachment=True
            ), 200

    return {"message": "Nome de arquivo invalido!"}, 404


def download_image_zip():
    file_extension = request.args.get('file_extension')
    compression_ratio = request.args.get('compression_ratio')
    
    if file_extension in ALLOWED_EXTENSIONS:  

        list_contents = len(os.listdir(f'{FILES_DIRECTORY}/{file_extension}'))

        if list_contents != 0:
            os.system(f'zip -r /tmp/{file_extension}.zip ./{FILES_DIRECTORY}/{file_extension} -{int(compression_ratio)}')

            return send_from_directory(
                directory='/tmp',
                path=f'{file_extension}.zip',
                as_attachment=True
            ), 200

        return {"message": "Arquivo não existente!"}, 404

    return {"message": "Formato de arquivo invalido!"}, 404
    