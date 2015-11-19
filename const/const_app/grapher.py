import pygal
from pygal.style import Style
import psycopg2
import unicodedata

def db_cursor():
    # TODO move
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    POSTGRES_DB = 'scrapper'
    POSTGRES_USER = 'scrapper'
    POSTGRES_PASS = 'scrapper'

    conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_USER, host=POSTGRES_HOST, port=POSTGRES_PORT)

    return conn.cursor()

def normalize(name):
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return name.lower()

def graph(username):

    labels, values = get_labels_and_values(username)

    s = Style(colors=('#5DA5DA', '#000000'))
    radar_chart = pygal.Radar(style = s)
    radar_chart.title = 'Emociones'
    radar_chart.x_labels = labels
    radar_chart.add('Candidato', values)
    g = radar_chart.render(fill = True)

    return g

def get_labels_and_values(username):

    cur = db_cursor()
    labels = []
    values = []

    try:
        cur.execute("SELECT * FROM proms WHERE idcandidato = (%s);",
                    (str(username).lower(),)
                    )
        rows = cur.fetchall()

        for row in rows:
            labels.append(row[1])
            values.append(row[2])

    except:
        print("Winning Eleven Error")

    return (labels, values)

def get_words_cloud(name):

    name = normalize(name)
    words = []

    cur = db_cursor()
    cur.execute("SELECT relacionado, cantidad FROM relaciones_candidatos WHERE nombre LIKE (%s) ",
                (name, ))
    rows = cur.fetchall()

    for row in rows:
        words << [row[0], row[1]]

    cur.execute("SELECT entidad, cantidad FROM candidatos_entidades WHERE nombre LIKE (%s) ",
                (name, ))
    rows = cur.fetchall()

    for row in rows:
        words << [row[0], row[1]]



    return words
