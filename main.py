import datetime
import json
from typing import Type
from utilities.griglia_di_liste_RO import Tabella2D_RO
from dateutil import parser as date_parser  #date_parse è una libreria che riconosce automaticamente tante formattazioni di date 



def valid_user_id(colonna: list[object]) -> bool:
    for elemento in colonna:
        try:
            n=int(elemento)
            if n >= 0:
                continue
            else:
                raise ValueError("L'identificativo dell'utente deve essere un numero intero non negativo")
        except ValueError:
            raise ValueError("L'identificativo dell'utente deve essere un numero intero non negativo")
    return True

def valid_data(colonna: list[object]) -> bool:
    for elemento in colonna:
        try:
            date_parser.parse(str(elemento)) #formattazione automatica della data 
            continue
        except (ValueError, TypeError):
            raise ValueError(f"La data '{elemento}' non è in un formato valido")
    return True

def valid_ip(colonna: list[object]) -> bool:
    for elemento in colonna:
        if not isinstance(elemento, str):
            raise TypeError("L'ip non è una stringa")
        else:
            if len([x for x in elemento.split('.')if x!=''])==4 and elemento.count('.')==3:
                continue
            raise TypeError("L'ip non è una stringa nel formato (x.x.x.x)")            
    return True

'''
def valid_tabella(tabella: Tabella2D_RO) -> bool:
    if not valid_user_id(tabella.get_colonna(1)):
        return False
    if not valid_data(tabella.get_colonna(0)):
        return False
    if not valid_ip(tabella.get_colonna(7)):
        return False
    if not valid_others(tabella):
        return False
    return True
'''

if __name__ == "__main__":
    try:
        json_data = json.load(open("test_data/test_small.json"))
    except Exception as e:
        print("Errore nel caricamento del file JSON: ", e)
        exit(1)

    
    tabella = Tabella2D_RO(json_data)
    print("Dimensioni della tabella: ", tabella.size())
    print("Elemento (0, 0): ", tabella.get_cell(0, 0))
    print("Riga 0: ", tabella.get_riga(0))
    print("Colonna 0: ", tabella.get_colonna(1))
    print("Validità degli user id: ", valid_user_id(tabella.get_colonna(1)))
    print("Valità delle date:", valid_data(tabella.get_colonna(0)))
    print("Valid ip:", valid_ip(tabella.get_colonna(7)))
    #valid_tabella(tabella)
    