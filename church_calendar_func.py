from datetime import date, timedelta
# uitgangsjaar
# algorithme van Carl Friedrich Gauss, gecorrigeerd overgenomen uit Wikipedia.

pentecost = timedelta(49, 0, 0)
ascension = timedelta(39, 0, 0)
week = timedelta(days=7)


def my_date_range(start, end, step=week):
    while start < end - step:
        yield start
        start += step

"""
bereken de paasdatum van enig jaar (de parameter kan zowel een datum als een integer zijn)
Berekening geschiedt volgens de algoritme van Gauss
"""

def get_easterdate(thedate):  #
    """calculates the easter date of the year of a given date, according to the algorithm by Gauss"""
    if isinstance(thedate, int):
        jaar = thedate
    else:
        jaar = thedate.year  # zie voorbeeld in wikipedia
    # bepaal gulden getal
    g = jaar % 19 + 1
    # bepaal de eeuw
    c = jaar // 100 + 1
    # corrigeer voor niet-schrikkeljaren
    x = (c * 3) // 4 - 12
    # maancorrectie
    y = (8 * c + 5) // 25 - 5
    # Zoek de zondag
    Z = (jaar * 5) // 4 - x - 10
    # bepaal epacta
    # 11 maal G + 20 + y. Trek daarvan x af, geheeldeel het resultaat door 30 en noem de rest E.
    # Als E gelijk is aan 24, of als E gelijk is aan 25 en het gulden getal is groter dan 11, tel dan 1 bij E op.
    # De Epacta voor 1991 is 14
    e = ((11 * g + 20 + y) - x) % 30
    if e == 24:
        e += 1
    elif (e == 25) and g > 11:
        e += 1
    n = 44 - e
    if n < 21:
        n += 30
    p = n + 7 - ((Z + n) % 7)
    if p > 31:
        p -= 31
        maand = 4
    else:
        maand = 3
        # print(P)
        # print(maand)
    pasen = date(jaar, maand, p)
    return pasen


def get_start_churchyear(thedate):
    """ berekent de datum van de eerste Advent van het jaar voorafgaand. 
       Deze dag valt 4 zondagen (maximaal 28 dagen) voor 25-12"""
    christmas = date(thedate.year - 1, 12, 25)
    toevoegendelta = timedelta(6 - christmas.weekday() - 28, 0,
                               0)  # maandag is 0, zondag is 6, aantal dagen tot volgende zondag
    advent1 = christmas + toevoegendelta
    return advent1


def get_end_churchyear(thedate):  # calculates the last Sunday of a churchyear, one week before the first of Advent
    if isinstance(thedate, int):
        x = date(thedate, 1, 1)
    else:
        x = thedate
    advent1 = get_start_churchyear(date(x.year + 1, 1, 1))
    return advent1 - week


def genereer_kerkelijk_jaar(thedate):
    """"genereer een list van data van te vieren zondagem en feestdagen """
    feestdagen = list()

    vorigjaar = thedate.year - 1
    christmas = date(vorigjaar, 12, 25)
    # Adventscyclus
    zondag = get_start_churchyear(thedate)
    feestdagen.append(zondag)
    while zondag < christmas - week:
        zondag += week
        feestdagen.append(zondag)
    feestdagen.append(christmas)  # Kerstmis

    pasen = get_easterdate(thedate)
    # print ("Easter on "+ pasen.strftime("%d %B %Y"))

    wittedonderdag = pasen - timedelta(days=3)
    # print(wittedonderdag)
    # genereer alle zondagen vanaf de zondag na Kerst tot en met Palmzondag  
    while zondag < wittedonderdag - week:
        zondag += week
        feestdagen.append(zondag)
        # print(zondag)
    # voeg de paascyclus toe
    feestdagen.append(wittedonderdag)
    # Goede Vrijdag
    feestdagen.append(wittedonderdag + timedelta(days=1))
    # Stille Zaterdag
    feestdagen.append(wittedonderdag + timedelta(days=2))
    # tel door tot Hemelvaart
    while zondag < pasen + ascension - week:
        zondag += week
        feestdagen.append(zondag)
    # print(zondag)
    # voeg Hemelvaart toe
    feestdagen.append(pasen + ascension)
    zondag += week
    feestdagen.append(zondag)
    pinksteren = pasen + pentecost

    eindekerkelijkjaar = get_end_churchyear(thedate)
    while zondag <= eindekerkelijkjaar - week:
        zondag += week
        feestdagen.append(zondag)
    return feestdagen
