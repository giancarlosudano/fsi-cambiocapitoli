import json
import os
# Percorso del file di input contenente le variabili di ambiente
input_file_path = os.path.join(".env")
output_file_path = os.path.join("env.json")

def convert_env_to_json(input_file, output_file):
    # Inizializza una lista vuota per contenere i dati JSON
    json_data = []
    
    # Apri il file di input per la lettura
    with open(input_file, 'r') as file:
        # Leggi ogni riga nel file
        for line in file:
            # Rimuovi gli spazi bianchi all'inizio e alla fine di ogni riga
            line = line.strip()
            # Ignora le righe vuote o i commenti
            if line and not line.startswith('#'):
                # Separa il nome della variabile e il valore
                name, value = line.split('=', 1)
                # Aggiungi l'elemento al JSON data
                json_data.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "slotSetting": False
                })
    
    # Scrivi i dati JSON nel file di output
    with open(output_file, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# Chiama la funzione per convertire il file
convert_env_to_json(input_file_path, output_file_path)

print(f'File convertito con successo in {output_file_path}')
