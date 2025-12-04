#!/bin/bash

# Script para executar o sistema completo
# Abre 3 terminais automaticamente

echo "🚀 Iniciando Sistema IoT..."
echo ""

# Verifica se ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute primeiro: ./install.sh"
    exit 1
fi

# Detecta qual terminal usar
if command -v gnome-terminal &> /dev/null; then
    TERMINAL="gnome-terminal"
elif command -v xterm &> /dev/null; then
    TERMINAL="xterm"
else
    echo "❌ Nenhum terminal compatível encontrado"
    echo "Execute manualmente conforme README.md"
    exit 1
fi

echo "✅ Iniciando componentes..."

# Terminal 1 - API
$TERMINAL -- bash -c "cd api && source ../venv/bin/activate && echo '🔵 Iniciando API REST na porta 8080...' && python app.py; exec bash" &

sleep 2

# Terminal 2 - Simulador
$TERMINAL -- bash -c "echo '🟢 Iniciando Simulador de Sensores...' && java -jar simulator-sensores-iot.jar; exec bash" &

sleep 2

# Terminal 3 - Dashboard
$TERMINAL -- bash -c "cd dashboard && source ../venv/bin/activate && echo '🟣 Iniciando Dashboard Streamlit...' && streamlit run app_streamlit.py; exec bash" &

echo ""
echo "✅ Sistema iniciado!"
echo ""
echo "📊 Acesse o dashboard em: http://localhost:8501"
echo ""
echo "Para parar: Feche os terminais ou pressione Ctrl+C em cada um"
