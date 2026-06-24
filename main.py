import httpx

# La lista che terrà tutta la conversazione: parte solo col system prompt
messaggi = [
    {"role": "system", "content": "Sei un pirata burbero. Rispondi sempre in italiano, breve e a tema piratesco."}
]

print("Parla col pirata (scrivi 'esci' per uscire)\n")

while True:
    domanda = input("Tu: ")
    if domanda == "esci":
        break

    # 1. Aggiungo il messaggio dell'utente alla conversazione
    messaggi.append({"role": "user", "content": domanda})

    # 2. Mando TUTTA la conversazione al modello
    risposta = httpx.post(
        "http://localhost:11434/api/chat",
        json={"model": "llama3.2", "messages": messaggi, "stream": False},
        timeout=60,
    )
    testo = risposta.json()["message"]["content"]

    # 3. Stampo la risposta E la salvo nella conversazione
    print("Pirata:", testo, "\n")
    messaggi.append({"role": "assistant", "content": testo})