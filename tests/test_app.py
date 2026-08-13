from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_abre_sem_excecoes():
    app = Path(__file__).resolve().parents[1] / "app.py"
    teste = AppTest.from_file(str(app), default_timeout=20).run()
    assert not teste.exception
    assert len(teste.tabs) == 5
