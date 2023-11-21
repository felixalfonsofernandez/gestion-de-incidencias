# app.py
from flask import Flask
from models import db_session, init_db
from werkzeug.middleware.profiler import ProfilerMiddleware
import os

app = Flask(__name__)

app.secret_key = 'una_llave_secreta_muy_segura'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Importa las rutas antes de envolver la aplicación con ProfilerMiddleware
from routes import *

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

if __name__ == '__main__':
    init_db()
    profiler_dir = os.path.join(os.getcwd(), 'profiler')
    if not os.path.exists(profiler_dir):
        os.mkdir(profiler_dir)
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir=profiler_dir)
    app.run(debug=True)
