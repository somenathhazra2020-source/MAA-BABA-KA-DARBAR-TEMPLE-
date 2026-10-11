from pathlib import Path
import ast

SOURCE = Path(__file__).with_name("bittu.py").read_text()

def test_source_parses():
    ast.parse(SOURCE)

def test_progress_table_created():
    assert "CREATE TABLE IF NOT EXISTS japa_progress" in SOURCE

def test_progress_scoped_by_temple():
    assert 'PRIMARY KEY(email, temple)' in SOURCE
    assert 'WHERE email=? AND temple=?' in SOURCE

def test_completed_mala_uses_transaction_and_history():
    assert 'def complete_japa_mala(email, temple):' in SOURCE
    assert 'INSERT INTO japa_history(email,count,created_at)' in SOURCE
    assert 'conn.rollback()' in SOURCE

def test_each_chant_persists_progress():
    assert 'save_japa_progress(st.session_state.email, st.session_state.active_temple, st.session_state.japa)' in SOURCE

def test_reset_persists_zero():
    assert 'save_japa_progress(st.session_state.email, st.session_state.active_temple, 0)' in SOURCE
