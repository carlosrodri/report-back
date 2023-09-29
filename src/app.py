from flask import Flask, jsonify
from flask_cors import CORS
from config import config
import pandas as pd
import json
import datetime

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
df_event = pd.read_csv('../data/Registro_Evento.csv',sep=',',encoding = "UTF-8")
df_event_students = df_event.drop(df_event[df_event['Programa_Academico'] == 'Docente'].index)
df_event_students = df_event.drop(df_event[df_event['Asignatura'].isnull() & (df_event.Programa_Academico == 'Docente')].index)
df_event_students = df_event.drop(df_event[df_event['Asignatura'].isnull()].index)
df_event_students = df_event.drop(df_event[df_event['Programa_Academico'] == 'Administrativo'].index)
df_event_students = df_event.drop(df_event[df_event['Programa_Academico'] == 'Gobernación de Boyacá'].index)

df_event_students['Correo'] = df_event_students['Correo'].str.lower()
df_event_students['Asignatura'] = df_event_students['Asignatura'].str.lower()
df_event_students.loc[df_event_students['Asignatura'].str.startswith('telem') & (df_event_students.Programa_Academico == 'Ingeniería Electrónica'), 'Asignatura'] = 'Telematica'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('comuni') & (df_event_students.Programa_Academico == 'Ingeniería Electrónica'), 'Asignatura'] = 'Comunicaciones 2' 
df_event_students.loc[df_event_students['Asignatura'].str.startswith('comuni') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Comunicaciones 2' 
df_event_students.loc[df_event_students['Asignatura'].str.startswith('comui') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Comunicaciones 2' 
df_event_students.loc[df_event_students['Asignatura'].str.startswith('transm') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Transmisión de Datos'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('investigaci') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Investigación de Operaciones'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('gest') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Gestión de redes'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('Gest') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Gestión de redes'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('arqu') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Arquitectura de Computadores'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('Semi') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Semillero Seguridad Telematics'
df_event_students.loc[df_event_students['Asignatura'].str.startswith('electiva iii') & (df_event_students.Programa_Academico == 'Ingeniería de Sistemas y Computación'), 'Asignatura'] = 'Electiva iii'



df_assitance1 = pd.read_csv('../data/2023-09-06 09_33.csv',sep=';',encoding = "UTF-8")

df_assitance2 = pd.read_csv('../data/2023-09-08 09_30.csv',sep=',',encoding = "UTF-8")

df_assitance3 = pd.read_csv('../data/2023-09-13 09_50.csv',sep=',',encoding = "UTF-8")

df_assitance4 = pd.read_csv('../data/2023-09-15 09_43.csv',sep=',',encoding = "UTF-8")

df_event_students['Session_1'] = df_event_students['Correo'].apply(lambda text: True if text in df_assitance1['Correo'].values else False)
df_event_students['Session_2'] = df_event_students['Correo'].apply(lambda text: True if text in df_assitance2['Correo'].values else False)
df_event_students['Session_3'] = df_event_students['Correo'].apply(lambda text: True if text in df_assitance3['Correo'].values else False)
df_event_students['Session_4'] = df_event_students['Correo'].apply(lambda text: True if text in df_assitance4['Correo'].values else False)


print(df_event_students)

df_students = df_event_students

print(df_students)

@app.route('/')
def index():
    parsed_json = json.loads(df_students.to_json(orient='records'))
    print(parsed_json)
  
    return jsonify({'assitance': parsed_json})

#Materias únicas
@app.route('/subject')
def subject():
    return jsonify({'Subjects': df_students['Asignatura'].unique().tolist()})

#Asistencia por asignatura
@app.route('/assistance-by-subject')
def assitanceBySubject():
    df_assitance = df_students.groupby(['Asignatura']).agg({'Session_1': 'sum', 'Session_2': 'sum', 'Session_3': 'sum', 'Session_4': 'sum'}).reset_index()
    parsed_json = json.loads(df_assitance.to_json(orient='records'))
    return jsonify({'Subjects': parsed_json})

#Top de materias por asistencia (descendente)
@app.route('/top-subject')
def topSubject():
    df_top_subject = df_students.groupby(['Asignatura']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').sort_values(by=['Total'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Materia con mayor asistencia  
@app.route('/top-subject-max')
def topSubjectMax():
    df_top_subject = df_students.groupby(['Asignatura']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').max()
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Materia con menor asistencia-----
@app.route('/top-subject-min')
def topSubjectMin():
    df_top_subject = df_students.groupby(['Asignatura']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').min()
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Estudiante con mayor asistencia
@app.route('/top-student-max')
def topStudentMax():
    df_top_subject = df_students.groupby(['Correo']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').max()
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Top asistencia por estudiante (descendente)-----
@app.route('/top-student')
def topStudent():
    df_top_subject = df_students.groupby(['Correo']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').sort_values(by=['Total'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Estudiante con menor asistencia    
@app.route('/top-student-min')
def topStudentMin():
    df_top_subject = df_students.groupby(['Correo']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').min()
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Top de asistencia por programa académico (descendente) -------
@app.route('/top-academic-program-assitance')
def topAcademnicProgram():
    df_top_subject = df_students.groupby(['Programa_Academico']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').sort_values(by=['Total'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json})

#Estudiantes sin asistencia
@app.route('/student-without-assistance')
def assitanceByStudent():
   df_top_subject = df_students.groupby(['Correo']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').min()
   parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
   return jsonify({'Subjects': parsed_json})

#Estudiantes por programa académico ---------
@app.route('/students-by-academic-program')
def StudentsByAcademicProgram():
    df_top_subject = df_students.groupby(['Programa_Academico']).apply(lambda x: x['Correo'].count()).reset_index(name='Total Estudiantes').sort_values(by=['Total Estudiantes'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'result': parsed_json})

#Programa académico con menos estudiantes
@app.route('/students-by-academic-program-min')
def StudentsByAcademicProgramMin():
    df_top_subject = df_students.groupby(['Programa_Academico']).apply(lambda x: x['Correo'].count()).reset_index(name='Total Estudiantes').sort_values(by=['Total Estudiantes'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'result': parsed_json[len(parsed_json) -1]})

#Programa académico con mas estudiantes --------
@app.route('/students-by-academic-program-max')
def StudentsByAcademicProgramMax():
    df_top_subject = df_students.groupby(['Programa_Academico']).apply(lambda x: x['Correo'].count()).reset_index(name='Total_Estudiantes').sort_values(by=['Total_Estudiantes'], ascending=False)
    parsed_json = json.loads(df_top_subject.to_json(orient='records'))
    
    return jsonify({'Subjects': parsed_json[0]})

@app.route('/assistance')
def assistance():
    df_event = pd.read_csv('../data/Registro_Evento.csv',sep=',',encoding = "UTF-8")
    
    df_fullAssitance = pd.merge(df_event, df_assitance1, on='Correo', how='inner')

    print(df_event)
    print(df_fullAssitance[df_fullAssitance['Programa_Academico'] == 'Ingeniería de Sistemas y Computación'])
    
    return jsonify({'assitance': df_fullAssitance.to_json()})
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=5001)

    
#reports
# 1- Asistencia por asiganatura √
# 2- Asistencia por estudiante √
# 3- Asistencia por programa academico √
# 4- Asigantura con mas asistencia √
# 5- Asigantura con menos asistencia √
# 7- Estudiantes sin asistencia √
# 8- Top 10 estudiantes con mas asistencia √
# 9- Top 10 estudiantes con menos asistencia √
# 10- Programa académico con mas asignaturas √
# 11- Programa académico con mas estudiantes √
# 12- Cantidad de estudiantes por programa académico √
# 13- Cantidad de estudiantes por asignatura √
# 6- Estudiante con mas horas de asistencia 
# 14- Horas promedio de asistencia por estudiante
# 15- Horas promedio de asistencia por asignatura
# 16- Promedio de asistencia por programa académico √