import os

PARAMS = {
    'UPLOAD_FOLDER': 'storage',
    'ALLOWED_EXTENSIONS': {'pdf'},
    'SECRET_KEY': os.environ['RE_SECRET_KEY'],
}