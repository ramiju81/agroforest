from pathlib import Path
import webbrowser
from datetime import datetime
import subprocess

# Configura tus rutas aquí (carpetas de proyectos, NO las .git)
RUTAS_PROYECTOS = [
    Path(r"C:\Users\julir\OneDrive\Proyectos\mySiss_Cloud_priv"),
    Path(r"C:\Users\julir\OneDrive\Proyectos\agroforest_priv"),
    Path(r"C:\Users\julir\OneDrive\Proyectos\messungen_priv")
]

class GitAnalyzer:
    def buscar_repositorios(self, rutas):
        """Busca repositorios Git en las rutas especificadas."""
        repos = []
        for ruta in rutas:
            if not ruta.exists():
                print(f"⚠️ Advertencia: Ruta no encontrada - {ruta}")
                continue
            
            # Busca recursivamente carpetas .git
            for git_dir in ruta.rglob('.git'):
                if git_dir.is_dir():
                    repos.append(str(git_dir.parent))
        
        return repos if repos else None

    @staticmethod
    def recuperar_archivos(ruta_repo):
        """Obtiene archivos no trackeados en un repositorio Git."""
        try:
            result = subprocess.run(
                ["git", "-C", str(ruta_repo), "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True
            )
            archivos = result.stdout.splitlines()
            return {
                "ruta": str(ruta_repo),
                "archivos_recuperables": archivos,
                "timestamp": datetime.now().isoformat()
            }
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error al recuperar archivos en {ruta_repo}: {e}")
            return {
                "ruta": str(ruta_repo),
                "archivos_recuperables": [],
                "timestamp": datetime.now().isoformat()
            }

def render_html(repos):
    """Genera el HTML del informe."""
    html_header = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Informe de Repositorios Git</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2c3e50; }
            .repo { background: #f8f9fa; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; }
            .file-list { margin-left: 20px; color: #7f8c8d; }
            .timestamp { font-size: 0.8em; color: #95a5a6; }
        </style>
    </head>
    <body>
        <h1>📋 Informe de Repositorios Git</h1>
    """

    html_body = ""
    analyzer = GitAnalyzer()
    for repo_path in repos:
        recovery_data = analyzer.recuperar_archivos(Path(repo_path))
        html_body += f"""
        <div class="repo">
            <h2>📁 {recovery_data['ruta']}</h2>
            <div class="timestamp">🕒 {recovery_data['timestamp']}</div>
            <h3>📝 Archivos recuperables:</h3>
            <ul class="file-list">
                {''.join(f'<li>{file}</li>' for file in recovery_data['archivos_recuperables'])}
            </ul>
        </div>
        """

    html_footer = """
    </body>
    </html>
    """

    return html_header + html_body + html_footer

def main():
    print("📋 Informe de Versionamiento GIT")
    print("🔍 Escaneando repositorios...")
    
    analyzer = GitAnalyzer()
    repos = analyzer.buscar_repositorios(RUTAS_PROYECTOS)
    
    if not repos:
        print("⚠️ No se encontraron repositorios Git. Verifica:")
        print("- Que las rutas en 'RUTAS_PROYECTOS' sean correctas.")
        print("- Que los proyectos tengan una carpeta '.git'.")
        return
    
    print(f"✅ Repositorios encontrados: {len(repos)}")
    for repo in repos:
        print(f"  → {repo}")
    
    # Genera el informe HTML
    html = render_html(repos)
    with open("informe_git.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    webbrowser.open("informe_git.html")
    print("📊 Informe generado: 'informe_git.html'")

if __name__ == "__main__":
    main()