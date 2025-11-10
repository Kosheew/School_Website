from flask import current_app
import re, os
import unicodedata

def secure_filename_unicode(filename):
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('utf-8', 'ignore').decode('utf-8')

    filename = re.sub(r'[^\w\s\-\.а-яА-ЯіІїЇєЄ]', '', filename)
    filename = filename.strip()

    name, ext = os.path.splitext(filename)
    return f"{name}{ext}"

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )
