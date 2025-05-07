import subprocess
from pathlib import Path
import os

class GitRecover:
    def __init__(self):
        self.recovery_dir = "recovery"  # Nombre fijo para la carpeta de recuperación
        
    def recover_file(self, repo_path: str, commit_hash: str, file_path: str):
        """Recupera un archivo específico desde un commit de Git"""
        try:
            # Convertir a rutas absolutas y normalizar
            repo_path = Path(repo_path).absolute()
            recovery_path = repo_path / self.recovery_dir / file_path
            
            # Crear directorios necesarios
            recovery_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Ejecutar comando Git
            cmd = [
                "git",
                "-C",
                str(repo_path),
                "show",
                f"{commit_hash}:{file_path}"
            ]
            
            result = subprocess.run(cmd, check=True, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            # Guardar el archivo recuperado
            recovery_path.write_text(result.stdout, encoding='utf-8')
            print(f"\n✓ Archivo recuperado exitosamente en: {recovery_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Error Git: {e.stderr.strip()}")
            return False
        except Exception as e:
            print(f"\n✗ Error inesperado: {str(e)}")
            return False

def main():
    print("=== Recuperación de archivos desde Git ===")
    print("Por favor proporcione la siguiente información:\n")
    
    # Obtener entrada del usuario
    repo_path = input("1. Ruta completa al repositorio Git: ").strip()
    commit_hash = input("2. Código del commit (hash Git): ").strip()
    file_path = input("3. Ruta relativa del archivo a recuperar: ").strip()
    
    # Validar entradas básicas
    if not all([repo_path, commit_hash, file_path]):
        print("\nError: Todos los campos son obligatorios.")
        return
    
    recover = GitRecover()
    
    print("\nProcesando la recuperación...")
    success = recover.recover_file(
        repo_path=repo_path,
        commit_hash=commit_hash,
        file_path=file_path
    )
    
    if success:
        print("\nOperación completada con éxito!")
    else:
        print("\nNo se pudo completar la operación. Verifique:")
        print("- Que la ruta del repositorio es correcta")
        print("- Que el hash del commit existe")
        print("- Que la ruta del archivo es correcta")
    
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()