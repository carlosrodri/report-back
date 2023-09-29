# report-back

## Instalación de dependencias

Dentro de la carpeta del proyecto ejecutar el comando `pip install -r requirements.txt` o `pip3 install -r requirements.txt` dependiendo de la versión de pip

## Ejecución del servidor:

Dentro de la carpeta src, ejecutar el comando: `python app.py` o `python3 app.py` dependindo de la cersion de python instalada

## Navegación dentro de las rutas

Dentro del archivo `app.py` se encuentra la lógica del programa y la API Rest diseñada en Flask, cada ruta es una consulta
y cada consulta tiene un comentario en el cual se espcifica a que hace referencia la consulta, por ejemplo:

`#Materia con mayor asistencia`

`@app.route('/top-subject-max')`

`def topSubjectMax():`
          
`df_top_subject = df_students.groupby(['Asignatura']).apply(lambda x: x['Session_1'].sum() + x['Session_2'].sum() + x['Session_3'].sum() + x['Session_4'].sum()).reset_index(name='Total').max()`
    
`parsed_json = json.loads(df_top_subject.to_json(orient='records'))`
    
  `return jsonify({'Subjects': parsed_json})`
