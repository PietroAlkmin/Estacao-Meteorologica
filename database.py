import sqlite3
import os

DATABASE_URL = 'dados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')  # espera até 5s
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

def inserir_leitura(temperatura, umidade, pressao=None):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
            (temperatura, umidade, pressao)
        )
        conn.commit()
        return cursor.lastrowid

def listar_leituras(limite=50):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?',
            (limite,)
        )
        
        linhas = cursor.fetchall()
        lista_de_leituras = []
        for linha in linhas:
            lista_de_leituras.append(dict(linha))
            
        return lista_de_leituras

def buscar_leitura(id_leitura):
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT * FROM leituras WHERE id = ?',
            (id_leitura,)
        )
        row = cursor.fetchone()
        
        if row != None:
            return dict(row)
        else:
            return None

def atualizar_leitura(id_leitura, dados):
    with get_db_connection() as conn:
        campos = []
        valores = []
        for chave, valor in dados.items():
            if chave in ['temperatura', 'umidade', 'pressao', 'localizacao']:
                campos.append(f"{chave} = ?")
                valores.append(valor)
        
        if not campos:
            return False
            
        valores.append(id_leitura)
        query = f"UPDATE leituras SET {', '.join(campos)} WHERE id = ?"
        
        conn.execute(query, valores)
        conn.commit()
        return True

def deletar_leitura(id_leitura):
    with get_db_connection() as conn:
        cursor = conn.execute('DELETE FROM leituras WHERE id = ?', (id_leitura,))
        conn.commit()
        return cursor.rowcount > 0

def estatisticas_leituras():
    with get_db_connection() as conn:
        cursor = conn.execute('''
            SELECT 
                AVG(temperatura) as media_temp, MIN(temperatura) as min_temp, MAX(temperatura) as max_temp,
                AVG(umidade) as media_umid, MIN(umidade) as min_umid, MAX(umidade) as max_umid
            FROM leituras
        ''')
        row = cursor.fetchone()
        
        if row != None:
            return dict(row)
        else:
            return None
