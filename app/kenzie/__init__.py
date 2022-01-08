import os
import dotenv

dotenv.load_dotenv()

FILES_DIRECTORY = os.environ.get('FILES_DIRECTORY')
MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH')
ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS').split(',')

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)

    for file_extension in ALLOWED_EXTENSIONS:
        file_path = os.path.join(FILES_DIRECTORY, file_extension)
        os.mkdir(file_path)
    