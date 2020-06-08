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
    sql = 'SELECT S1."Nome" AS Squadra1, S2."Nome" AS Squadra2, P."Stadio", P."Fase", S3."Nome" AS SquadraVincente, P."Data" \
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

    sql = 'SELECT "Stagione" FROM Campionato WHERE "ID" = %s'
    cursor.execute(sql, [str(id)])
    campionato = cursor.fetchone()
    print(classifica)
    return render_template("campionato.html", partite=partite, classifica=classifica, campionato=campionato[0])

# PAGINA CHE MOSTRA INFORMAZIONI APPROFONDITE RISPETTO AD UNA PARTITA


@app.route("/partita/<partita>", methods=["GET"])
def partita(partita):

    return render_template("campionato.html")


if __name__ == "__main__":
    app.run(debug=True)
