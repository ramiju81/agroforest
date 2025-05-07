from pathlib import Path
from core.analyzer import GitAnalyzer

def render_html(repos):
    """Genera el HTML del informe a partir de los repositorios encontrados."""
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
    for repo_path in repos:
        recovery_data = GitAnalyzer.recuperar_archivos(Path(repo_path))
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