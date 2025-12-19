"""
Sistema Keep-Alive para Replit
Mantém o bot online através de um servidor Flask
"""
from flask import Flask
from threading import Thread
from config import KEEP_ALIVE_PORT

app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot Discord está online e funcionando!"

@app.route('/status')
def status():
    return {"status": "online", "message": "Bot operacional"}

def run():
    """Inicia o servidor Flask em modo silencioso"""
    app.run(host='0.0.0.0', port=KEEP_ALIVE_PORT, debug=False)

def keep_alive():
    """Inicia o keep-alive em uma thread separada"""
    t = Thread(target=run, daemon=True)
    t.start()
    print(f"✅ Keep-alive ativo na porta {KEEP_ALIVE_PORT}")