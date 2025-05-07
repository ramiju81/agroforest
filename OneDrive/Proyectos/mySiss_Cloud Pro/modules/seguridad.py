import os
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException

# Inicialización de BD
def init_db():
    conn = sqlite3.connect('database.db')
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
        clave_actualizada TIMESTAMP,
        intentos_fallidos INTEGER DEFAULT 0,
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
            0  # No necesita cambiar clave inicial
        ))
    
    conn.commit()
    conn.close()

# Funciones de seguridad
def hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + key.hex()

def verify_password(stored_hash: str, password: str) -> bool:
    salt = bytes.fromhex(stored_hash[:64])
    key = bytes.fromhex(stored_hash[64:])
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return new_key == key

def authenticate_user(username: str, password: str) -> dict:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, username, password_hash, rol, bloqueado, debe_cambiar_clave 
    FROM usuarios WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(user[2], password):
        return None
    
    if user[4]:  # bloqueado
        raise HTTPException(status_code=400, detail="Cuenta bloqueada")
    
    return {
        "id": user[0],
        "username": user[1],
        "rol": user[3],
        "debe_cambiar_clave": bool(user[5])
    }