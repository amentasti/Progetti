### 5. Il giro del mondo in 80 giorni

# Consideriamo il [dataset](http://island.ricerca.di.unimi.it/~alfio/shared/worldcities.xlsx) che descrive alcune delle principali 
# città del mondo. Supponiamo che sia sempre possibile viaggiare da ciascuna città alle 3 città più vicine e che tale viaggio 
# richieda 2 ore per la città più vicina, 4 ore per la seconda città più vicina e 8 ore per la terza città più vicina. 
# Inoltre, il viaggio dura altre 2 ore se la città di destinazione si trova in un Paese diverso da quello di partenza e altre 2 ore 
# se la città di destinazione ha più di 200.000 abitanti.

# Partendo da Londra e viaggiando sempre verso est, è possibile fare il giro del mondo tornando a Londra in 80 giorni? 
# Quanto tempo richiede almeno?



#Importiamo pandas per la gestione dei dati e math per eseguire calcoli matematici
import pandas as pd
import math

# Leggiamo il file Excel e creiamo il DataFrame
file_worldcities = 'C:\\Users\\Admin\\OneDrive\\Desktop\\Data Science\\Programming with Python\\worldcities.xlsx'
df = pd.read_excel(file_worldcities)

# Formattiamo le colonne di latitudine e longitudine come numeri decimali
df['lat'] = df['lat'].astype(float)
df['lng'] = df['lng'].astype(float)

# Per rendere più verosimile il cammino che dovremmo  percorrere, andiamo a prendere le città che hanno latitudine +/- 3 
# rispetto a Londra (51)
df = df[df['lat'].astype(int).isin([48, 49, 50, 51, 52, 53, 54])]

# Per semplificare il calcolo prendiamo solo la parte intera della latitudine e della longitudine
df['lat_int'] = df['lat'].astype(int)
df['lng_int'] = df['lng'].astype(int)

# Convertiamo il DataFrame in una lista di dizionari, dove ogni dizionario rappresenta una città
cities = df.to_dict(orient='records')

# Per risolvere il problema della continuita longitudinale (+180/-180) creiamo una lista aggiuntiva con longitudini positive e 
# negative convertite
extended_cities = []
for city in cities:
    extended_cities.append(city)
    if city['lng_int'] < 0:
        city_copy = city.copy()
        city_copy['lng_int'] += 360  # Trasforma le longitudini negative in positive
        extended_cities.append(city_copy)

# Per calcolare la distanza tra le città usiamo il teorema di pitagora considerando la continuità longitudinale
def pitagora_distance(lat1, lon1, lat2, lon2):
    delta_lon = lon2 - lon1
    if abs(delta_lon) > 180:  # Considera la continuità longitudinale
        delta_lon = 360 - abs(delta_lon)
    return math.sqrt((lat2 - lat1) ** 2 + delta_lon ** 2)

# Imponiamo che lo spostamento alla città più vicina possa essere fatto solo verso est
def find_closest_city(city, cities, visited_cities):
    closest_city = None
    min_distance = float('inf')
    for target in cities:
        if target != city and target['city'] not in visited_cities:      #Imponiamo che non sia tra le città già visitate
            if target['lng_int'] > city['lng_int']:
                distance = pitagora_distance(city['lat_int'], city['lng_int'], target['lat_int'], target['lng_int'])
                if distance < min_distance:
                    min_distance = distance
                    closest_city = target
    return closest_city

# Calcoliamo la funzione per il tempo di viaggio, imponendo tutte le condizioni su distanza, paese e popolazione
def travel_time(from_city, to_city):
    distance = pitagora_distance(from_city['lat_int'], from_city['lng_int'], to_city['lat_int'], to_city['lng_int'])
    if distance == 0:
        return 0  # Non ci si sposta
    if distance <= 1:          # Condizioni sulla distanza
        time = 2
    elif distance <= 2:
        time = 4
    else:
        time = 8
    if from_city['country'] != to_city['country']:     # Condizioni sul paese
        time += 2
    if to_city['population'] > 200000:      # Condizioni sulla popolazione
        time += 2
    return time

# Troviamo la città di partenza (Londra)
start_city = next(city for city in cities if city['city'] == 'London')

# Simuliamo il viaggio con un ciclo while 
def simulate_journey(start_city, cities):
    current_city = start_city
    visited_cities = set()
    visited_cities_list = []
    total_time = 0
    while True:
        visited_cities.add(current_city['city'])          #Aggiungiamo la città corrente alle città visitate
        visited_cities_list.append(current_city['city'])
        closest_city = find_closest_city(current_city, cities, visited_cities)   #Troviamo la città più vicina verso est
        if closest_city is None:                      #Se non ci sono più città da visitare usciamo dal ciclo
            break
        travel = travel_time(current_city, closest_city)        #Calcoliamo il tempo di viaggio tra le 2 città e sommiamo al totale
        total_time += travel
        current_city = closest_city
        if current_city['city'] == start_city['city'] and len(visited_cities) == len(cities):   #Controlliamo se la città corrente è la città di partenza e se tutte le città nella lista cities sono state visitate. Se entrambe le condizioni sono vere, esce dal ciclo
            break        
    
    return total_time, visited_cities_list

# Simulazione del viaggio a partire da Londra
total_travel_time, visited_cities_list = simulate_journey(start_city, extended_cities)




print("Città visitate nel viaggio:")
print(" -> ".join(visited_cities_list))
print(f"Durata totale del viaggio: {total_travel_time} ore")
print(f"È possibile completare il giro del mondo in 80 giorni? {'Sì' if total_travel_time <= 80*24 else 'No'}")






