from pathlib import Path

def save_html_report(html_content: str, filename: str):
    """Guarda el informe HTML en un archivo"""
    try:
        filepath = Path(filename)
        filepath.write_text(html_content, encoding='utf-8')
        print(f"✅ Informe guardado en: {filepath.absolute()}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar el informe: {e}")
        return False