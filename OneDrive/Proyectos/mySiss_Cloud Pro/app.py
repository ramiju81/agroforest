import os
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import uvicorn

app = FastAPI()

# Configuración de archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Funciones de Seguridad ---
def hash_password(password: str) -> str:
    """Genera un hash seguro de la contraseña"""
    salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + key.hex()

def verify_password(stored_hash: str, password: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado"""
    salt = bytes.fromhex(stored_hash[:64])
    key = bytes.fromhex(stored_hash[64:])
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_key == key

def get_db_connection():
    """Crea y retorna una conexión a la base de datos"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos si no existe"""
    if not os.path.exists('database.db'):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            celular TEXT,
            rol TEXT NOT NULL,
            debe_cambiar_clave BOOLEAN DEFAULT 1,
            bloqueado BOOLEAN DEFAULT 0,
            creado_por INTEGER,
            FOREIGN KEY (creado_por) REFERENCES usuarios (id)
        )
        ''')
        
        # Insertar superadmin si no existe
        cursor.execute('SELECT 1 FROM usuarios WHERE username="ramiju"')
        if not cursor.fetchone():
            password_hash = hash_password("16931356")
            cursor.execute('''
            INSERT INTO usuarios 
            (username, password_hash, email, celular, rol, debe_cambiar_clave) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                "ramiju", 
                password_hash, 
                "juliram81@hotmail.com", 
                "3183863532", 
                "superadmin",
                0
            ))
        
        conn.commit()
        conn.close()

# Inicializar la base de datos al iniciar
init_db()

# --- Middleware de Autenticación ---
async def get_current_user(request: Request):
    """Obtiene el usuario actual basado en las cookies de sesión"""
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, username, rol FROM usuarios WHERE id = ?", 
        (user_id,)
    ).fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return dict(user)

# --- Rutas Principales ---
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Muestra la página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Procesa el formulario de login"""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, username, password_hash, rol FROM usuarios WHERE username = ?", 
        (username,)
    ).fetchone()
    conn.close()
    
    if not user or not verify_password(user["password_hash"], password):
        return RedirectResponse("/?error=Credenciales+incorrectas", status_code=303)
    
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(key="user_id", value=str(user["id"]))
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(get_current_user)):
    """Muestra el panel principal"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user
    })

# --- Rutas de Configuración ---
@app.get("/configuracion/usuarios", response_class=HTMLResponse)
async def config_usuarios(
    request: Request, 
    user: dict = Depends(get_current_user)
):
    """Muestra la gestión de usuarios"""
    if user["rol"] not in ["superadmin", "mySiss"]:
        return RedirectResponse("/dashboard?error=Sin+permisos", status_code=303)
    
    conn = get_db_connection()
    usuarios = conn.execute("SELECT id, username, email, rol FROM usuarios").fetchall()
    conn.close()
    
    return templates.TemplateResponse("configuracion/usuarios.html", {
        "request": request,
        "user": user,
        "usuarios": usuarios
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)