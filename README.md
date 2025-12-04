# Sistema IoT - Monitoramento de Sensores

Sistema completo para coleta, armazenamento e visualização de dados de sensores IoT.

**Avaliação 04 - Sistemas Distribuídos**  
**Data:** 27 de novembro de 2025

---

## 📋 Descrição

Este projeto implementa uma solução completa de sistemas distribuídos composta por:

- **API REST** em Python (Flask) - Recebe e armazena dados dos sensores
- **Banco de Dados SQLite** - Persistência dos dados
- **Dashboard Streamlit** - Visualização interativa dos dados em tempo real
- **Simulador de Sensores** - Gerador de dados IoT (fornecido)

---

## 🎯 Funcionalidades

### API REST (Flask)
- ✅ Endpoint `POST /api/sensor/data` - Recebe dados dos sensores
- ✅ Endpoint `GET /api/sensor/data` - Lista todas as leituras
- ✅ Endpoint `GET /api/sensor/summary` - Última leitura por sensor
- ✅ Endpoint `GET /api/sensor/stats` - Estatísticas agregadas
- ✅ Armazenamento em SQLite
- ✅ CORS habilitado

### Dashboard (Streamlit)
- ✅ Cards com última leitura de cada sensor
- ✅ Tabela com histórico de leituras
- ✅ Estatísticas em tempo real
- ✅ Atualização automática a cada 5 segundos
- ✅ Interface responsiva

### Tipos de Sensores
- 🌡️ **Temperatura** (T0xx) - em °C
- 💧 **Umidade** (H0xx) - em %
- 💡 **Luminosidade** (L0xx) - em lux
- 🚶 **Movimento** (M0xx)

---

## 📁 Estrutura do Projeto

```
API_Rest/
├── api/
│   ├── app.py              # API REST Flask
│   └── sensor_data.db      # Banco SQLite (criado automaticamente)
├── dashboard/
│   └── app_streamlit.py    # Dashboard Streamlit
├── venv/                   # Ambiente virtual (criado pelo install.sh)
├── simulator-sensores-iot.jar  # Simulador de sensores (fornecido)
├── requirements.txt        # Dependências Python
├── install.sh              # Script de instalação
├── run.sh                  # Script para executar tudo
└── README.md              # Este arquivo
```

---

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8 ou superior
- Java JRE 8 ou superior
- Linux/Mac (para scripts .sh) ou Windows com WSL

### Opção 1: Instalação Automática (Linux/Mac)

```bash
# Dar permissão de execução
chmod +x install.sh run.sh

# Executar instalação
./install.sh

# Executar o sistema
./run.sh
```

### Opção 2: Instalação Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt
```

---

## 🎮 Como Executar

### Executar Manualmente (3 terminais)

**Terminal 1 - API REST:**
```bash
cd api
source ../venv/bin/activate
python app.py
```
> API disponível em: http://localhost:8080

**Terminal 2 - Simulador:**
```bash
java -jar simulator-sensores-iot.jar
```
> Envia dados automaticamente para a API

**Terminal 3 - Dashboard:**
```bash
cd dashboard
source ../venv/bin/activate
streamlit run app_streamlit.py
```
> Dashboard disponível em: http://localhost:8501

---

## 🧪 Testando a API

### Testar com curl:

```bash
# Listar todas as leituras
curl http://localhost:8080/api/sensor/data

# Resumo dos sensores
curl http://localhost:8080/api/sensor/summary

# Estatísticas
curl http://localhost:8080/api/sensor/stats

# Enviar dados manualmente
curl -X POST http://localhost:8080/api/sensor/data \
  -H "Content-Type: application/json" \
  -d '{"sensorId":"T999","type":"temperature","value":25.5,"timestamp":"2025-12-04T10:00:00Z"}'
```

### Testar no navegador:
- http://localhost:8080/api/sensor/data
- http://localhost:8080/api/sensor/summary

---

## 📊 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/sensor/data` | Recebe dados dos sensores |
| GET | `/api/sensor/data?limit=N` | Lista leituras (padrão: 1000) |
| GET | `/api/sensor/summary` | Última leitura por sensor |
| GET | `/api/sensor/stats` | Estatísticas agregadas |

### Formato JSON (POST):
```json
{
  "sensorId": "T010",
  "type": "temperature",
  "value": 23.5,
  "timestamp": "2025-12-04T14:32:55Z"
}
```

---

## 🗃️ Esquema do Banco de Dados

```sql
CREATE TABLE sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensorId TEXT NOT NULL,
    value REAL NOT NULL,
    timestamp TEXT NOT NULL
);
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask 3.0.0** - Framework web para API REST
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing
- **SQLite** - Banco de dados leve (integrado ao Python)

### Frontend
- **Streamlit 1.29.0** - Framework para dashboards em Python
- **Pandas 2.1.4** - Manipulação de dados
- **Requests 2.31.0** - Requisições HTTP

---

## 📸 Demonstração

### Dashboard Streamlit mostra:
1. **Cards coloridos** com última leitura de cada sensor
2. **Tabela interativa** com histórico de leituras
3. **Estatísticas** em tempo real (total, média, etc.)
4. **Status da API** (Online/Offline)
5. **Atualização automática** a cada 5 segundos

---

## ✅ Checklist de Requisitos Atendidos

- [x] API REST funcional na porta 8080
- [x] Endpoint `/api/sensor/data` recebendo POST
- [x] Persistência em banco SQLite
- [x] Armazenamento de sensorId, value e timestamp
- [x] Dashboard consumindo a API via HTTP
- [x] Listagem de leituras
- [x] Visualização de última leitura por sensor
- [x] Interface clara e funcional
- [x] Código bem estruturado e comentado
- [x] Atualização em tempo real

---

## 🐛 Solução de Problemas

### Porta 8080 já em uso:
```bash
# Verificar processo usando a porta
lsof -i :8080

# Matar processo
kill -9 <PID>
```

### Erro ao instalar dependências:
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar novamente
pip install -r requirements.txt
```

### Dashboard não conecta na API:
- Verifique se a API está rodando em http://localhost:8080
- Verifique se o simulador está enviando dados
- Confira os logs no terminal da API

---

## 👥 Autores

[Adicione aqui os nomes dos integrantes do grupo]

---

## 📅 Informações do Projeto

- **Disciplina:** Sistemas Distribuídos
- **Avaliação:** Avaliação IV
- **Pontuação:** 50 pontos
- **Data de Entrega:** 27 de novembro de 2025

---

## 📝 Licença

Projeto acadêmico desenvolvido para fins educacionais.
