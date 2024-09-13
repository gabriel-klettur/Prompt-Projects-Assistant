# tests/test_file_utils.py

from src.utils.file_utils import extrae_contenido_archivos

def test_extrae_contenido_archivos(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("Contenido de prueba 1")
    archivos = [str(file1)]
    contenido = extrae_contenido_archivos(archivos)
    assert "Contenido de prueba 1" in contenido
