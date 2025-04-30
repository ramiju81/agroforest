from flask import Flask, render_template
import os
from pathlib import Path

# Ruta ABSOLUTA a tu proyecto
PROJECT_PATH = Path(r"C:\Users\julir\OneDrive\Messungen\prueba_flask")

app = Flask(__name__, template_folder=PROJECT_PATH/"templates")

@app.route('/')
def home():
    # Depuración (verás esto en la terminal)
    print(f"\n⭐ Ruta templates: {app.template_folder}")
    print(f"⭐ Archivos: {os.listdir(app.template_folder)}\n")
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)