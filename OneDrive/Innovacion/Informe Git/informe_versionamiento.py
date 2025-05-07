from pathlib import Path
import webbrowser
from datetime import datetime
import subprocess
from templates import render_html

# Configura tus rutas aquí (carpetas de proyectos, NO las .git)
RUTAS_PROYECTOS = [
    Path(r"C:\Users\julir\OneDrive\Proyectos\mySiss_Cloud"),
    Path(r"C:\Users\julir\OneDrive\Proyectos\agroforest"),
    Path(r"C:\Users\julir\OneDrive\Proyectos\messungen")
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