import os
import subprocess
from pathlib import Path
from typing import List, Dict
import shutil

class GitAnalyzer:
    @staticmethod
    def get_repo_info(repo_path: Path) -> Dict:
        """Obtiene información del repo y archivos eliminados"""
        def run_git(cmd):
            try:
                result = subprocess.run(
                    ['git', '-C', str(repo_path)] + cmd,
                    capture_output=True, text=True
                )
                return result.stdout.strip() if result.returncode == 0 else ""
            except:
                return ""

        # Obtener archivos eliminados
        lost_files = []
        log_output = run_git(["log", "--all", "--full-history", "--diff-filter=D", "--name-only", "--pretty=format:%H"])
        current_file = None
        for line in log_output.splitlines():
            if line:
                if len(line) == 40:  # Hash de commit
                    current_file = None
                elif current_file is None:  # Archivo eliminado
                    current_file = line.strip()
                    lost_files.append({
                        'commit': line,
                        'path': current_file,
                        'extension': os.path.splitext(current_file)[1]
                    })

        return {
            'nombre': repo_path.name,
            'ruta': str(repo_path),
            'rama': run_git(["branch", "--show-current"]),
            'commits': run_git(["log", "--pretty=format:%h - %s (%cr)", "-3"]).split('\n'),
            'estado': run_git(["status", "--short"]),
            'archivos_eliminados': lost_files
        }

    @staticmethod
    def buscar_repositorios(rutas: List[Path]) -> List[Dict]:
        """Busca repositorios manteniendo estructura original"""
        repos = []
        for ruta in rutas:
            ruta = Path(ruta)
            if (ruta/".git").exists():
                repos.append(GitAnalyzer.get_repo_info(ruta))
            