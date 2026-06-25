import httpx
import json
from datetime import datetime

def che_ora_e():
    return datetime.now().strftime("%H:%M")

funzioni_disponibili = {
    "che_ora_e": che_ora_e,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "che_ora_e",
            "description": "Restituisce l'ora attuale nel formato ore:minuti",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    }
]

messaggi = [
    {"role": "system", "content": "Sei un assistente che usa gli strumenti forniti. Quando ricevi il risultato di uno strumento, usalo per rispondere direttamente all'utente, senza dire che non hai accesso ai dati in tempo reale."},
    {"role": "user", "content": "Che ore sono?"},
]

# --- GIRO 1 ---
r1 = httpx.post(
    "http://localhost:11434/api/chat",
    json={"model": "llama3.2", "messages": messaggi, "tools": tools, "stream": False},
    timeout=60,
)
print(r1)
messaggio = r1.json()["message"]
messaggi.append(messaggio)
print(messaggio)
# --- ESEGUO gli strumenti ---
for chiamata in messaggio["tool_calls"]:
    nome = chiamata["function"]["name"]
    argomenti = chiamata["function"]["arguments"]
    funzione = funzioni_disponibili[nome]
    risultato = funzione(**argomenti)
    print(f"[eseguito {nome}() -> {risultato}]")
    messaggi.append({"role": "tool", "tool_name": nome, "content": risultato})

# --- GIRO 2 ---
r2 = httpx.post(
    "http://localhost:11434/api/chat",
    json={"model": "llama3.2", "messages": messaggi, "stream": False},
    timeout=60,
)
print(r2.json()["message"]["content"])