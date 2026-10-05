"""
Sistem de Gestiune Casă Inteligentă (Procedural / Fără OOP)
Tipuri de echipamente:
1. iluminat     -> parametru: luminozitate (0-100%)
2. climatizare  -> parametru: temperatura_tinta (15-30 °C)
3. securitate   -> parametru: armat (True/False)
"""

def creeaza_sistem():
    return {}

def inregistreaza_echipament(sistem, id_eq, tip, denumire, stare_initiala):
    if id_eq in sistem:
        return False, f"Eroare: ID-ul '{id_eq}' există deja în sistem."
    
    tipuri_valide = {"iluminat", "climatizare", "securitate"}
    if tip not in tipuri_valide:
        return False, f"Eroare: Tipul '{tip}' nu este suportat."

    sistem[id_eq] = {
        "tip": tip,
        "denumire": denumire,
        "stare": dict(stare_initiala)
    }
    return True, f"Echipamentul '{denumire}' ({id_eq}) a fost înregistrat."

def citeste_stare(sistem, id_eq):
    if id_eq not in sistem:
        return None, f"Echipamentul cu ID-ul '{id_eq}' nu a fost găsit."
    return sistem[id_eq], "Succes"

def trimite_comanda(sistem, id_eq, comanda, valoare=None):
    if id_eq not in sistem:
        return False, f"Comandă eșuată: ID-ul '{id_eq}' nu există."
    
    stare = sistem[id_eq]["stare"]
    tip = sistem[id_eq]["tip"]

    if comanda == "pornire":
        stare["activ"] = True
        return True, f"'{id_eq}' a fost pornit."
    elif comanda == "oprire":
        stare["activ"] = False
        return True, f"'{id_eq}' a fost oprit."
    elif comanda == "seteaza_parametru":
        if tip == "iluminat" and "luminozitate" in stare:
            if 0 <= valoare <= 100:
                stare["luminozitate"] = valoare
                return True, f"Luminozitate setată la {valoare}% pentru '{id_eq}'."
            return False, "Valoare invalidă pentru luminozitate (0-100)."
        
        elif tip == "climatizare" and "temperatura_tinta" in stare:
            if 15.0 <= valoare <= 30.0:
                stare["temperatura_tinta"] = float(valoare)
                return True, f"Temperatură setată la {valoare}°C pentru '{id_eq}'."
            return False, "Valoare invalidă pentru temperatură (15-30 °C)."
        
        elif tip == "securitate" and "armat" in stare:
            stare["armat"] = bool(valoare)
            return True, f"Stare armare setată la {stare['armat']} pentru '{id_eq}'."

    return False, f"Comandă necunoscută sau parametru incompatibil: '{comanda}'."

def agregare_sistem(sistem):
    numar_echipamente = len(sistem)
    echipamente_active = sum(1 for eq in sistem.values() if eq["stare"].get("activ", False))
    consum_total_w = sum(
        eq["stare"].get("consum_w", 0) 
        for eq in sistem.values() 
        if eq["stare"].get("activ", False)
    )
    return {
        "total_echipamente": numar_echipamente,
        "echipamente_active": echipamente_active,
        "consum_total_activ_w": consum_total_w
    }

def listeaza_echipamente(sistem):
    print("\n" + "=" * 70)
    print(f"{'ID':<12} | {'DENUMIRE':<20} | {'TIP':<13} | {'ACTIV':<6} | PARAMETRI")
    print("-" * 70)
    for id_eq, date in sistem.items():
        stare = date["stare"]
        activ = "DA" if stare.get("activ") else "NU"
        
        # Filtram parametrii specifici
        params = [f"{k}: {v}" for k, v in stare.items() if k not in ("activ", "consum_w")]
        params.append(f"Consum: {stare.get('consum_w', 0)}W")
        detalii = ", ".join(params)
        
        print(f"{id_eq:<12} | {date['denumire']:<20} | {date['tip']:<13} | {activ:<6} | {detalii}")
    print("=" * 70)


# ==============================================================================
# DEMONSTRAȚIE LIVE CU DATE DE TEST
# ==============================================================================
if __name__ == "__main__":
    hub = creeaza_sistem()

    print(">>> 1. Înregistrare echipamente de test...")
    inregistreaza_echipament(hub, "light_liv", "iluminat", "Lustră Living", {
        "activ": True, "luminozitate": 80, "consum_w": 40
    })
    inregistreaza_echipament(hub, "light_dorm", "iluminat", "Veioză Dormitor", {
        "activ": False, "luminozitate": 50, "consum_w": 10
    })
    inregistreaza_echipament(hub, "ac_main", "climatizare", "Aer Condiționat", {
        "activ": True, "temperatura_tinta": 22.5, "consum_w": 1200
    })
    inregistreaza_echipament(hub, "alarm_zone", "securitate", "Sistem Alarmă Perimetru", {
        "activ": True, "armat": True, "consum_w": 15
    })

    print("\n>>> 2. Listarea completă a echipamentelor:")
    listeaza_echipamente(hub)

    print("\n>>> 3. Trimitere comenzi către echipamente:")
    _, msg = trimite_comanda(hub, "light_dorm", "pornire")
    print("  ->", msg)
    _, msg = trimite_comanda(hub, "light_dorm", "seteaza_parametru", 100)
    print("  ->", msg)
    _, msg = trimite_comanda(hub, "ac_main", "seteaza_parametru", 24.0)
    print("  ->", msg)
    _, msg = trimite_comanda(hub, "alarm_zone", "seteaza_parametru", False)
    print("  ->", msg)

    print("\n>>> 4. Citirea stării unui singur echipament ('ac_main'):")
    echipament, _ = citeste_stare(hub, "ac_main")
    print(f"  Denumire: {echipament['denumire']}")
    print(f"  Stare curentă: {echipament['stare']}")

    print("\n>>> 5. Agregare la nivel de sistem:")
    statistici = agregare_sistem(hub)
    print(f"  Total echipamente monitorizate: {statistici['total_echipamente']}")
    print(f"  Echipamente active în acest moment: {statistici['echipamente_active']}")
    print(f"  Consum energetic cumulat (doar active): {statistici['consum_total_activ_w']} W")

    print("\n>>> Listare finală după aplicarea comenzilor:")
    listeaza_echipamente(hub)