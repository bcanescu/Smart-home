


def inregistreaza_echipament(sistem,id,tip,stare_initiala,denumire):
    if id in sistem:
        return False,f"Id-ul '{id}' exista deja in sistem!"
    tipuri_permise = ["climatizare","securitate","iluminat"]
    if tip not in tipuri_permise:
        return False,"tipul introdus nu este permis"
    sistem[id] = {
        "tip" : tip,
        "id" : id,
        "stare" : dict(stare_initiala),
        "denumire":denumire
    }
    return True,f"echipamentul '{denumire}' a fost salvat"
def citire_stare(sistem, id):
    if id not in sistem:
        return False, "Id nu este in sistem"
    return True, sistem[id]["stare"]
def trimite_comanda(sistem,id,comanda,valoare = None):
    if id not in sistem:
        return False,"id nu a fost gasit"
    stare = sistem[id]["stare"]
    tip = sistem[id]["tip"]
    if comanda == "pornire":
        stare["activ"] = True
        return True,f"echipamentul '{id}' a fost pornit"
    elif comanda == "oprire":
            stare["activ"] = False
            return True,f"echipamentul '{id}' a fost oprit"
    elif comanda == "seteaza_parametru":
        if tip == "iluminat" and "luminozitate" in stare:
            if 0<=valoare<=100:
                stare["luminozitate"] = valoare
                return True,f"luminozitate setata la {valoare} % pentru '{id}'"
            return False,"valoare invalida"
        elif tip == "climatizare" and "temperatura" in stare:
            if 0<=valoare<=35:
                stare["temperatura"] = valoare
                return True,f"temperatura setata la {valoare} grade pentru '{id}'"
            return False,"valoare invalida"
        elif tip == "securitate" and "armat" in stare:
            stare["armat"]= bool(valoare)
            return True, f"statusul de armare a fost setat pe {stare['armat']} pentru '{id}'"
    return False,"comanda gresita sau parametru necunoscut"
def agregare_sistem(sistem):
    total = len(sistem)
    active = 0
    consum_total = 0
    for date in sistem.values():
        stare = date["stare"]
        if stare["activ"]==True :
            active = active + 1
            consum_total = consum_total + stare["consum_w"]
    return {
        "total": total,
        "active": active,
        "consum_total_w": consum_total
    }
def listeaza_echipamente(sistem):
    for id,date in sistem.items():
        denumire = date["denumire"]
        tip = date["tip"]
        stare = date["stare"]
        status = "Pornit" if stare["activ"]==True else "Oprit"
        print(f"[{id}] {denumire} ({tip}) -> Status: {status} | Parametri: {stare}")



def testare():
    casa = {}

    print("Adaugare ")
    inregistreaza_echipament(casa, "bec1", "iluminat", {"activ": False, "luminozitate": 50, "consum_w": 10}, "Bec Hol")
    inregistreaza_echipament(casa, "ac1", "climatizare", {"activ": True, "temperatura": 24, "consum_w": 1200}, "Aer Condiționat")
    inregistreaza_echipament(casa, "alarma1", "securitate", {"activ": True, "armat": True, "consum_w": 15}, "Senzor Mișcare")

    listeaza_echipamente(casa)

    print("Comenzi")
    trimite_comanda(casa, "bec1", "pornire")
    trimite_comanda(casa, "bec1", "seteaza_parametru", 90)
    trimite_comanda(casa, "ac1", "seteaza_parametru", 21)


    print(" Citire stare  ")
    gasit, date = citire_stare(casa, "bec1")
    print(f"Stare bec1: {date}")

    print(" Stare tot sistemul ")
    statistici = agregare_sistem(casa)
    print(f"Total aparate: {statistici['total']}")
    print(f"Aparate pornite: {statistici['active']}")
    print(f"Consum total: {statistici['consum_total_w']} W")

testare()