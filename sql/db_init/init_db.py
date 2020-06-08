from psycopg2 import connect
from faker import Faker
import random

# Semplice funzione che ritorna un Codice Fiscale casuale


def fake_cf():
    cf = ''
    for n in range(6):
        cf += chr(random.randint(65, 90))

    for n in range(2):
        cf += str(random.randint(0, 9))

    cf += chr(random.randint(65, 90))

    for n in range(2):
        cf += str(random.randint(0, 9))

    cf += chr(random.randint(65, 90))

    for n in range(3):
        cf += str(random.randint(0, 9))

    cf += chr(random.randint(65, 90))

    return cf


database = connect(user="postgres", password="z", host="localhost",
                   port="5432", database="almanacco_calcistico")
faker = Faker('it_IT')

cursor = database.cursor()

# INIZIO INSERT CALCIATORI

# CANCELLA TUTTI I DATI DA CALCIATORE
cursor.execute('DELETE FROM public.Calciatore')
database.commit()

sql = 'INSERT INTO public.Calciatore ("CF", "Nome", "Cognome", "Numero") VALUES (%s, %s, %s, %s)'
calciatori = []

n = 0
while n < 100:
    nomecognome = faker.name_male().split(' ')
    if len(nomecognome) == 2:
        calciatore = {
            "CF": fake_cf(),
            "Nome": nomecognome[0],
            "Cognome": nomecognome[1]
        }
        cursor.execute(sql, (calciatore["CF"], calciatore["Nome"],
                             calciatore["Cognome"], str(random.randint(10, 99))))
        n += 1

database.commit()

# FINE INSERT CALCIATORI

# INIZIO INSERT SQUADRE

# cursor.execute('DROP TABLE public.Squadra')
# cursor.execute('CREATE TABLE public.Squadra ("ID" SERIAL NOT NULL, "Nome" VARCHAR(50) NOT NULL, "Stagione" VARCHAR(9) NOT NULL, "Punti" INT NOT NULL, PRIMARY KEY ("ID"));')
database.commit()

squadre = (
    # 1999/2000
    ('Juventus', '1999/2000', 9),
    ('Milan', '1999/2000', 6),
    ('Inter', '1999/2000', 3),
    ('Torino', '1999/2000', 0),
    ('Hellas Verona', '1999/2000', 0),
    ('Chievo', '1999/2000', 3),
    ('Roma', '1999/2000', 0),
    ('Lazio', '1999/2000', 0),

    # 2000/2001
    ('Juventus', '2000/2001', 6),
    ('Milan', '2000/2001', 3),
    ('Inter', '2000/2001', 3),
    ('Torino', '2000/2001', 0),
    ('Hellas Verona', '2000/2001', 9),
    ('Chievo', '2000/2001', 0),
    ('Roma', '2000/2001', 0),
    ('Lazio', '2000/2001', 0),

    # 2001/2002
    ('Juventus', '2001/2002', 0),
    ('Milan', '2001/2002', 3),
    ('Inter', '2001/2002', 9),
    ('Torino', '2001/2002', 3),
    ('Hellas Verona', '2001/2002', 6),
    ('Chievo', '2001/2002', 0),
    ('Roma', '2001/2002', 0),
    ('Lazio', '2001/2002', 0)

)

sql = 'INSERT INTO public.Squadra ("Nome", "Stagione", "Punti") VALUES (%s, %s, %s)'
cursor.executemany(sql, squadre)

database.commit()

# FINE INSERT SQUADRE

# INIZIO ASSOCIAZIONE SQUADRA - CALCIATORE

cursor.execute('SELECT * FROM public.Calciatore')
calciatori = cursor.fetchall()
squadre = {
    # 1999/2000
    1: calciatori[0:11],
    2: calciatori[11:22],
    3: calciatori[22:33],
    4: calciatori[33:44],
    5: calciatori[44:55],
    6: calciatori[55:66],
    7: calciatori[66:77],
    8: calciatori[77:88],

    # 2000/2001
    9: calciatori[3:14],
    10: calciatori[14:25],
    11: calciatori[25:36],
    12: calciatori[36:47],
    13: calciatori[47:58],
    14: calciatori[58:69],
    15: calciatori[69:80],
    16: calciatori[80:91],

    # 2001/2002
    17: calciatori[11:22],
    18: calciatori[22:33],
    19: calciatori[33:44],
    20: calciatori[44:55],
    21: calciatori[55:66],
    22: calciatori[66:77],
    23: calciatori[77:88],
    24: calciatori[88:99],
}

sql = 'INSERT INTO public.calciatoresquadra VALUES (%s, %s)'
for key in squadre.keys():
    for calciatore in squadre[key]:
        cursor.execute(sql, (calciatore[0], key))
database.commit()

# FINE ASSOCIAZIONE SQUADRA - CALCIATORE

# INIZIO INSERT CAMPIONATO

# cursor.execute('DROP TABLE public.Campionato')
# cursor.execute('CREATE TABLE public.Campionato ("ID" SERIAL NOT NULL, "Stagione" VARCHAR (9) NOT NULL, PRIMARY KEY ("ID"));')
database.commit()

cursor.execute(
    'INSERT INTO public.Campionato ("Stagione") VALUES (\'1999/2000\')')
cursor.execute(
    'INSERT INTO public.Campionato ("Stagione") VALUES (\'2000/2001\')')
cursor.execute(
    'INSERT INTO public.Campionato ("Stagione") VALUES (\'2001/2002\')')

database.commit()

# FINE INSERT CAMPIONATO

# INIZIO INSERT PARTITE

# 1999/2000
cursor.execute(
    'INSERT INTO public.Partita VALUES (1, 4, \'1999-01-22\', \'Juventus Stadium\', 1, 1, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (2, 5, \'1999-01-29\', \'SanSiro Stadium\', 2, 1, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (3, 7, \'1999-02-05\', \'SanSiro Stadium\', 3, 1, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (6, 8, \'1999-02-12\', \'Bentegodi Stadium\', 6, 1, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (2, 3, \'1999-02-18\', \'SanSiro Stadium\', 2, 1, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (1, 6, \'1999-02-25\', \'Juventus Stadium\', 1, 1, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (1, 2, \'1999-03-04\', \'Juventus Stadium\', 1, 1, \'Finale\')')

# 2000/2001
cursor.execute(
    'INSERT INTO public.Partita VALUES (10, 16, \'2000-01-22\', \'SanSiro Stadium\', 10, 2, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (11, 15, \'2000-01-29\', \'SanSiro Stadium\', 11, 2, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (12, 13, \'2000-02-05\', \'Juventus Stadium\', 13, 2, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (9, 14, \'2000-02-12\', \'Juventus Stadium\', 9, 2, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (13, 11, \'2000-02-18\', \'Bentegodi Stadium\', 2, 2, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (9, 10, \'2000-02-25\', \'Juventus Stadium\', 9, 2, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (13, 9, \'2000-03-04\', \'Bentegodi Stadium\', 13, 2, \'Finale\')')

# 2001/2002
cursor.execute(
    'INSERT INTO public.Partita VALUES (20, 22, \'2001-01-22\', \'Juventus Stadium\', 20, 3, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (24, 18, \'2001-01-29\', \'Stadio Olimpico\', 18, 3, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (21, 23, \'2001-02-05\', \'Bentegodi Stadium\', 21, 3, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (19, 17, \'2001-02-12\', \'SanSiro Stadium\', 19, 3, \'Quarti di Finale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (18, 19, \'2001-02-18\', \'SanSiro Stadium\', 19, 3, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (21, 20, \'2001-02-25\', \'Bentegodi Stadium\', 21, 3, \'Semifinale\')')
cursor.execute(
    'INSERT INTO public.Partita VALUES (21, 19, \'2001-03-04\', \'Bentegodi Stadium\', 19, 3, \'Finale\')')
database.commit()
# FINE INSERT PARTITE

database.close()
