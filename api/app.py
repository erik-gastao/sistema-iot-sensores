# API REST para Sistema IoT de Sensores
# Autor: Erik Gastão
# Sistemas Distribuídos - 2025

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), 'sensor_data.db')

def init_db():
    """Cria o banco de dados e a tabela se não existir"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria a tabela para armazenar as leituras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensorId TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado")

@app.route('/api/sensor/data', methods=['POST'])
def receive_sensor_data():
    """Endpoint que recebe dados dos sensores IoT"""
    try:
        # Pega o JSON enviado pelo simulador
        data = request.get_json()
        
        # Valida se os campos obrigatórios existem
        if not data or 'sensorId' not in data or 'value' not in data or 'timestamp' not in data:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        # Extrai os valores
        sensor_id = data['sensorId']
        value = data['value']
        timestamp = data['timestamp']
        
        # Conecta no banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insere os dados na tabela
        cursor.execute('''
            INSERT INTO sensor_readings (sensorId, value, timestamp)
            VALUES (?, ?, ?)
        ''', (sensor_id, value, timestamp))
        
        # Salva as mudanças
        conn.commit()
        conn.close()
        
        print(f"Dados recebidos: {sensor_id} = {value}")
        
        return jsonify({
            'status': 'success',
            'message': 'Dados armazenados com sucesso'
        }), 201
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensor/data', methods=['GET'])
def get_sensor_data():
    """Endpoint para o dashboard consultar os dados"""
    try:
        # Pega parâmetro opcional de limite
        limit = request.args.get('limit', 100, type=int)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Busca os últimos registros
        cursor.execute('''
            SELECT id, sensorId, value, timestamp
            FROM sensor_readings
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Converte para lista de dicionários (JSON)
        readings = []
        for row in rows:
            readings.append({
                'id': row[0],
                'sensorId': row[1],
                'value': row[2],
                'timestamp': row[3]
            })
        
        return jsonify(readings), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sensor/summary', methods=['GET'])
def get_sensor_summary():
    """Endpoint que retorna a última leitura de cada sensor"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Busca a última leitura de cada sensor
        cursor.execute('''
            SELECT sensorId, value, timestamp, MAX(id)
            FROM sensor_readings
            GROUP BY sensorId
            ORDER BY sensorId
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        summary = []
        for row in rows:
            summary.append({
                'sensorId': row[0],
                'lastValue': row[1],
                'lastTimestamp': row[2]
            })
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    print("API iniciando...")
    print("Aguardando dados em http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)