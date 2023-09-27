from flask import Flask, jsonify
from config import config
import pandas as pd
import numpy as np 
import array

app = Flask(__name__)


@app.route('/')
def index():
    df_event = pd.read_csv('../data/Registro_Evento.csv',sep=',',encoding = "UTF-8")

    studentList = df_event[df_event.Programa_Academico == 'Ingeniería de Sistemas y Computación'][["Nombre", "Programa_Academico"]]
    
    print(studentList)
    
    # print( np.asarray(studentList).flatten())
  
    return jsonify({'students': []})
    
@app.route('/assitance')
def assistance():
    df_event = pd.read_csv('../data/Registro_Evento.csv',sep=',',encoding = "UTF-8")
    
    df_assitance1 = pd.read_csv('../data/2023-09-15 09_43.csv',sep=',',encoding = "UTF-8")
    df_assitance2 = pd.read_csv('../data/2023-09-13 09_50.csv',sep=',',encoding = "UTF-8")
    df_assitance3 = pd.read_csv('../data/2023-09-08 09_30.csv',sep=',',encoding = "UTF-8")
    df_assitance4 = pd.read_csv('../data/2023-09-06 09_33.csv',sep=',',encoding = "UTF-8")
    
    fullAssitance = pd.merge(df_event, df_assitance1, how='outer')

    print(fullAssitance.to_json())
    
    return jsonify({'assitance': fullAssitance.to_json()})
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=5001)

    
#reports
# 1- Asistencia por asiganatura
# 2- Asistencia por estudiante
# 3- Asistencia por programa academico
# 4- Asigantura con mas asistencia
# 5- Asigantura con menos asistencia
# 6- Estudiante con mas horas de asistencia
# 7- Estudaintes sin asistencia
# 8- Top 10 estudiantes con mas asistencia
# 9- Top 10 estudiantes con menos asistencia
# 10- Programa académico con mas asignaturas
# 11- Programa académico con mas estudiantes
# 12- Cantidad de estudiantes por programa académico
# 13- Cantidad de estudiantes por asignatura
# 14- Horas promedio de asistencia por estudiante
# 15- Horas promedio de asistencia por asignatura
# 16- Promedio de asistencia por programa académico