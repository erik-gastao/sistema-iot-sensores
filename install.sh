#!/bin/bash

# Script de instalação e configuração do Sistema IoT
# Avaliação 04 - Sistemas Distribuídos

echo "================================================"
echo "   Sistema IoT - Instalação e Configuração"
echo "================================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python 3.x"
    exit 1
fi

echo "✅ Python3 encontrado"

# Verifica se Java está instalado
if ! command -v java &> /dev/null; then
    echo "❌ Java não encontrado. Por favor, instale Java JRE"
    exit 1
fi

echo "✅ Java encontrado"
echo ""

# Cria ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "================================================"
echo "   Como executar o sistema:"
echo "================================================"
echo ""
echo "1. Terminal 1 - API REST:"
echo "   cd api"
echo "   source ../venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. Terminal 2 - Simulador de Sensores:"
echo "   java -jar simulator-sensores-iot.jar"
echo ""
echo "3. Terminal 3 - Dashboard:"
echo "   cd dashboard"
echo "   source ../venv/bin/activate"
echo "   streamlit run app_streamlit.py"
echo ""
echo "================================================"
echo "Ou use: ./run.sh para iniciar automaticamente"
echo "================================================"
