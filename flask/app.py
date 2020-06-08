# STRAMBINI ENEA CL. 5AI A.S. 2019/2020
# SVOLGIMENTO ELABORATO INDIVIDUALE DI INFORMATICA

from flask import Flask, render_template
from psycopg2 import connect
import datetime

app = Flask(__name__)

database = connect(
    user="postgres",
    password="z",
    host="localhost",
    port="5432",
    database="almanacco_calcistico"
)
cursor = database.cursor()

# HOMEPAGE


@app.route("/")
def home():
    cursor.execute('SELECT * FROM public.Campionato')
    data = cursor.fetchall()

    return render_template("home.html", data=data)

# PAGINA CHE MOSTRA LE FASI A GIRONI E LA CLASSIFICA FINALE DI UN CAMPIONATO


@app.route("/campionato/<int:id>", methods=["GET"])
def campionato(id):
    sql = 'SELECT S1."Nome" AS Squadra1, S2."Nome" AS Squadra2, P."Fase", S3."Nome" AS SquadraVincente, P."IDSquadra1", P."IDSquadra2"\
            FROM Squadra AS S1, Squadra AS S2, Squadra AS S3, Partita AS P \
            WHERE P."IDSquadra1" = S1."ID" AND P."IDSquadra2" = S2."ID" AND P."Vincitore" = S3."ID" AND P."Campionato" = %s\
            ORDER BY P."Data" ASC'
    cursor.execute(sql, [str(id)])
    partite = cursor.fetchall()

    sql = 'SELECT S."Nome", S."Punti" \
            FROM Squadra AS S, Campionato AS C \
            WHERE C."Stagione" = S."Stagione" AND C."ID" = %s \
            ORDER BY S."Punti" DESC'
    cursor.execute(sql, [str(id)])
    classifica = cursor.fetchall()

    sql = 'SELECT * FROM Campionato WHERE "ID" = %s'
    cursor.execute(sql, [str(id)])
    campionato = cursor.fetchone()

    return render_template("campionato.html", partite=partite, classifica=classifica, campionato=campionato)

# PAGINA CHE MOSTRA INFORMAZIONI APPROFONDITE RISPETTO AD UNA PARTITA


@app.route("/partita/<int:id1>/<int:id2>/<int:idcampionato>", methods=["GET"])
def partita(id1, id2, idcampionato):

    # QUERY CHE RITORNA I DATI DELLA PARTITA SELEZIONATA
    sql = 'SELECT S1."Nome" AS Squadra1, S2."Nome" AS Squadra2, P."Fase", S3."Nome" AS SquadraVincente, P."Stadio", P."Data"\
            FROM Squadra AS S1, Squadra AS S2, Squadra AS S3, Partita AS P \
            WHERE P."IDSquadra1" = S1."ID" AND P."IDSquadra2" = S2."ID" AND P."Vincitore" = S3."ID" AND P."Campionato" = %s\
            AND S1."ID" = %s AND S2."ID" = %s ORDER BY P."Data" ASC'
    cursor.execute(sql, [str(idcampionato), str(id1), str(id2)])
    partita = cursor.fetchone()

    # QUERY CHE ASSOCIA I CALCIATORI ALLE SQUADRE
    sql = 'SELECT C."Nome", C."Cognome", C."Numero" \
            FROM Calciatore AS C, CalciatoreSquadra AS CS, Campionato AS CM, Squadra AS S \
            WHERE CS."CF" = C."CF" AND CS."IDSquadra" = S."ID" AND \
                S."Stagione" = CM."Stagione" AND S."ID" = %s AND CM."ID" = %s'

    # Associazione Giocatori - Squadra 1
    cursor.execute(sql, [str(id1), str(idcampionato)])
    squadra1 = {
        "nome": partita[0],
        "giocatori": cursor.fetchall()
    }

    # Associazione Giocatori - Squadra 2
    cursor.execute(sql, [str(id2), str(idcampionato)])
    squadra2 = {
        "nome": partita[1],
        "giocatori": cursor.fetchall()
    }

    return render_template("partita.html", squadra1=squadra1, squadra2=squadra2, partita=partita)


if __name__ == "__main__":
    app.run(debug=True)
