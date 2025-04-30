from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from pyngrok import ngrok, conf
from dotenv import load_dotenv
import os
from pathlib import Path  # <-- Añade esto

# Configuración inicial
app = Flask(__name__)

# --------------------------
# Configuración MEJORADA de la base de datos:
# 1. Para desarrollo local
if os.environ.get('FLASK_ENV') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messungen.db'
# 2. Para la versión ejecutable (.exe)
else:
    # Windows: AppData/Local/Messungen
    # Linux/macOS: ~/.local/share/Messungen
    db_dir = Path.home() / 'AppData' / 'Local' / 'Messungen' if os.name == 'nt' else Path.home() / '.local' / 'share' / 'Messungen'
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / 'messungen.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# --------------------------

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
app.config['STATIC_FOLDER'] = 'static'

db = SQLAlchemy(app)

# ---- AÑADE ESTA RUTA JUSTO AQUÍ ----
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)
# -----------------------------------

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150))
    correo = db.Column(db.String(150), unique=True)
    contraseña = db.Column(db.String(150))
    origen = db.Column(db.String(50))  # google o manual

# Crear tablas
with app.app_context():
    db.create_all()

# Configuración de ngrok (opcional, solo para desarrollo)
load_dotenv()
ngrok_token = os.getenv("NGROK_AUTHTOKEN")
if ngrok_token:
    conf.get_default().auth_token = ngrok_token
    public_url = ngrok.connect(5000)
    print("🌐 Tu app está disponible en:", public_url)

# Rutas de autenticación
@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contraseña = request.form['password']
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['usuario'] = usuario.correo
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Credenciales incorrectas")
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        contraseña = request.form['password']
        
        if Usuario.query.filter_by(correo=correo).first():
            return render_template('registro.html', error="El correo ya está registrado")
        
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contraseña=generate_password_hash(contraseña),
            origen="manual"
        )
        db.session.add(usuario)
        db.session.commit()
        
        session['usuario'] = correo
        return redirect(url_for('dashboard'))
    return render_template('registro.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        # Aquí implementarías el reseteo de contraseña
        return render_template('reset.html', message="Se ha enviado un enlace para resetear tu contraseña")
    return render_template('reset.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = Usuario.query.filter_by(correo=session['usuario']).first()
    return f"Hola {usuario.nombre} 👋 Bienvenido a tu panel."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)