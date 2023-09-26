from flask import Flask
from config import config
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    df_event = pd.read_csv('../data/Registro_Evento.csv',sep=',',encoding = "UTF-8")

    print(df_event[df_event.Programa_Academico == 'Ingeniería de Sistemas y Computación'][["Nombre","Programa_Academico"]])

    return 'Hello World!'

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=5001)