import datetime
import json
from utilities.griglia_di_liste_RO import Tabella2D_RO
from dateutil import parser as date_parser  #date_parse è una libreria che riconosce automaticamente tante formattazioni di date 


def valid_user_id(colonna: list[object]) -> bool:
    '''
    Ritorna True se gli id sono validi
    '''
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
    '''
    Ritorna True se le date sono valide
    '''
    for elemento in colonna:
        try:
            date_parser.parse(str(elemento)) #formattazione automatica della data 
            continue
        except (ValueError, TypeError):
            raise ValueError(f"La data '{elemento}' non è in un formato valido")
    return True

def valid_ip(colonna: list[object]) -> bool:
    '''
    Ritorna True se gli ip sono validi
    '''    
    for elemento in colonna:
        if not isinstance(elemento, str):
            raise TypeError("L'ip non è una stringa")
        else:
            if len([x for x in elemento.split('.')if x!=''])==4 and elemento.count('.')==3:
                continue
            print("Elemento:", elemento)
            raise TypeError(f"L'ip {elemento} non è una stringa nel formato (x.x.x.x)")            
    return True

def valid_others(colonna: list[object]) -> bool:
    '''
    Ritorna True se tutte le altre colonne sono valide
    '''    
    for elemento in colonna:
        if not isinstance(elemento, str):
            raise TypeError("La colonna non è una stringa")
    return True


def valid_tabella(tabella: Tabella2D_RO) -> bool:
    '''
    Funzione che valida tutta la tabella
    '''
    if not valid_user_id(tabella.get_colonna(1)):
        return False
    if not valid_data(tabella.get_colonna(0)):
        return False
    if not valid_ip(tabella.get_colonna(7)):
        return False
    for i in range(2,7):    
        valid_others(tabella.get_colonna(i))
    return True

def first_access(tabella,user_id):
    temp = min([datetime.datetime.strptime(x, "%d/%m/%Y %H:%M") for x in tabella.get_colonna(0) if tabella.get_colonna(1)[tabella.get_colonna(0).index(x)]==user_id])
    res = temp.strftime("%d/%m/%Y %H:%M")
    return res

def last_access(tabella,user_id):
    temp = max([datetime.datetime.strptime(x, "%d/%m/%Y %H:%M") for x in tabella.get_colonna(0) if tabella.get_colonna(1)[tabella.get_colonna(0).index(x)]==user_id])
    res = temp.strftime("%d/%m/%Y %H:%M")
    return res

def num_access(tabella,user_id):
    res = len([x for x in tabella.get_colonna(0) if tabella.get_colonna(1)[tabella.get_colonna(0).index(x)]==user_id])
    return res

if __name__ == "__main__":
    try:
        json_data = json.load(open("test_data/test_small.json"))
    except Exception as e:
        print("Errore nel caricamento del file JSON: ", e)
        exit(1)

    tabella = Tabella2D_RO(json_data)
    valid_tabella(tabella)

    users={x for x in tabella.get_colonna(1)}
    final_tab = [[user,first_access(tabella, user),last_access(tabella, user),num_access(tabella, user)] for user in users]

    print("Final Table:", final_tab)
