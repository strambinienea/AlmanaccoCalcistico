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
    ('juventus', '1999/2000', 9),
    ('milan', '1999/2000', 6),
    ('inter', '1999/2000', 3),
    ('torino', '1999/2000', 0),
    ('hellas verona', '1999/2000', 0),
    ('chievo', '1999/2000', 3),
    ('roma', '1999/2000', 0),
    ('lazio', '1999/2000', 0)
)

sql = 'INSERT INTO public.Squadra ("Nome", "Stagione", "Punti") VALUES (%s, %s, %s)'
cursor.executemany(sql, squadre)

database.commit()

# FINE INSERT SQUADRE

# INIZIO ASSOCIAZIONE SQUADRA - CALCIATORE

cursor.execute('SELECT * FROM public.Calciatore')
calciatori = cursor.fetchall()
squadre = {
    1: calciatori[0:11],
    2: calciatori[12:23],
    3: calciatori[24:35],
    4: calciatori[36:47],
    5: calciatori[48:59],
    6: calciatori[60:71],
    7: calciatori[72:83],
    8: calciatori[84:95]
}

sql = 'INSERT INTO public.calciatoresquadra VALUES (%s, %s)'
# print(squadre.keys())
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
database.commit()

# FINE INSERT CAMPIONATO

# INIZIO INSERT PARTITE
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

database.commit()
# FINE INSERT PARTITE

database.close()
