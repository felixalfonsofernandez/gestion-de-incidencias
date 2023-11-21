# routes.py
from datetime import datetime
from flask import render_template, request, redirect, url_for, session
from app import app  # Importa la instancia de la aplicación que creaste
from models import Usuario, db_session, Jefe, Tareas,DataSynLab # Importa tus modelos y sesión de db
import tensorflow as tf
from sqlalchemy import case
from sqlalchemy import func, cast, Date, text
from flask_mail import Mail, Message
from sqlalchemy import literal_column
import pandas as pd
import joblib
import json
from flask import render_template, jsonify

# model = tf.keras.models.load_model('regresion_logistica.h5')
# Cargar el modelo entrenado
modelo = joblib.load('modelo_entrenado_random_forest.joblib')


# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'pruebasynlab5@gmail.com'
app.config['MAIL_PASSWORD'] = 'hsxy iuke syer xksw'
app.config['MAIL_DEFAULT_SENDER'] = 'gustavoadolfo.alania@unmsm.edu.pe'

mail = Mail(app)

@app.route('/')
def bienvenida():
    return render_template('bienvenida.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    email_data = request.json
    email = email_data.get('email')
    subject = email_data.get('subject', 'No Subject')
    content = email_data.get('content', 'No Content')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Crear el mensaje
    msg = Message(subject, recipients=[email])
    msg.body = content
    # Enviar el mensaje
    mail.send(msg)

    return jsonify({"message": "Email sent successfully to {}".format(email)}), 200

# ... (otras rutas y funciones de vistas)

@app.route('/guardar-ticket', methods=['POST'])
def guardar_ticket():
    # Extraer los datos del formulario
    # Utiliza request.form.get('nombre_campo') si esperas que alguno pueda estar vacío
    tipo_ticket = request.form['tipo_ticket']
    area = request.form['area']
    # Extrae el resto de los campos aquí...

    # Obtener el valor más alto de Ticket y sumarle uno
    max_ticket = db_session.query(func.max(DataSynLab.Ticket)).scalar()
    if max_ticket is None:
        max_ticket = 0
    nuevo_numero_ticket = max_ticket + 1

    
    nuevo_ticket = DataSynLab(
        Ticket=nuevo_numero_ticket,
        Tipo_Ticket=tipo_ticket,
        Area=area,
        Id_Solicitante=request.form['id_solicitante'],
        Mail_Solicitante=session['email_usuario'],
        Solicitante=request.form['solicitante'],
        Cargo=request.form['cargo'],
        Centro_de_costos=request.form['centro_de_costos'],
        Area1=request.form['area1'],
        Gerencia=request.form['gerencia'],
        Local=request.form['local'],
        Titulo=request.form['titulo'],
        Categoría=request.form['categoria'],
        Sub_Categoria=request.form['sub_categoria'],
        Aplicacion_Servicio=request.form['aplicacion_servicio'],
        Prioridad=request.form['prioridad'],
        Fecha_Registro=request.form['fecha_registro'],
        Fecha_Estado=request.form['fecha_estado'],
        Dias_Espera=request.form['dias_espera'],
        Dias_Laborales=request.form['dias_laborales'],
        Estado=request.form['estado'],
        Id_Ejecutor=request.form['id_ejecutor'],
        Cta_Ejecutor=request.form['cta_ejecutor'],
        Ejecutor=request.form['ejecutor']
    )

    try:
        db_session.add(nuevo_ticket)
        db_session.commit()

        subject = "Nuevo Ticket Guardado"
        content = (f"Detalles del Ticket:\n"
                   f"Tipo: {tipo_ticket}\n"
                   f"Área: {area}\n"
                   f"Solicitante: {nuevo_ticket.Solicitante}\n"
                   f"Cargo: {nuevo_ticket.Cargo}\n"
                   f"Título: {nuevo_ticket.Titulo}\n")
        msg = Message(subject, recipients=[nuevo_ticket.Mail_Solicitante])
        msg.body = content
        mail.send(msg)

        return jsonify({'mensaje': 'Ticket guardado y correo enviado con éxito'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/guardar-ticket-2', methods=['POST'])
def guardar_ticket_2():
    # Extraer los datos del formulario
    # Utiliza request.form.get('nombre_campo') si esperas que alguno pueda estar vacío
    tipo_ticket = request.form['tipo_ticket']
    area = request.form['area']
    # Extrae el resto de los campos aquí...

    # Obtener el valor más alto de Ticket y sumarle uno
    max_ticket = db_session.query(func.max(DataSynLab.Ticket)).scalar()
    if max_ticket is None:
        max_ticket = 0
    nuevo_numero_ticket = max_ticket + 1

    
    nuevo_ticket = DataSynLab(
        Ticket=nuevo_numero_ticket,
        Tipo_Ticket=tipo_ticket,
        Area=area,
        Id_Solicitante=request.form['id_solicitante'],
        Mail_Solicitante=session['email'],
        Solicitante=request.form['solicitante'],
        Cargo=request.form['cargo'],
        Centro_de_costos=request.form['centro_de_costos'],
        Area1=request.form['area1'],
        Gerencia=request.form['gerencia'],
        Local=request.form['local'],
        Titulo=request.form['titulo'],
        Categoría=request.form['categoria'],
        Sub_Categoria=request.form['sub_categoria'],
        Aplicacion_Servicio=request.form['aplicacion_servicio'],
        Prioridad=request.form['prioridad'],
        Fecha_Registro=request.form['fecha_registro'],
        Fecha_Estado=request.form['fecha_estado'],
        Dias_Espera=request.form['dias_espera'],
        Dias_Laborales=request.form['dias_laborales'],
        Estado=request.form['estado'],
        Id_Ejecutor=request.form['id_ejecutor'],
        Cta_Ejecutor=request.form['cta_ejecutor'],
        Ejecutor=request.form['ejecutor']
    )

    try:
        db_session.add(nuevo_ticket)
        db_session.commit()

        subject = "Nuevo Ticket Guardado"
        content = (f"Detalles del Ticket:\n"
                   f"Tipo: {tipo_ticket}\n"
                   f"Área: {area}\n"
                   f"Solicitante: {nuevo_ticket.Solicitante}\n"
                   f"Cargo: {nuevo_ticket.Cargo}\n"
                   f"Título: {nuevo_ticket.Titulo}\n")
        msg = Message(subject, recipients=[nuevo_ticket.Mail_Solicitante])
        msg.body = content
        mail.send(msg)

        return jsonify({'mensaje': 'Ticket guardado y correo enviado con éxito'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    


@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    # Verifica si el usuario ya está logueado
    if 'usuario' in session:
        return redirect(url_for('tareas'))

    mensaje_error = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Consulta la base de datos para verificar las credenciales
        usuario_valido = db_session.query(Usuario).filter_by(Usuario=usuario, Contraseña=contraseña).first()

        if usuario_valido:
            session['usuario'] = usuario  # Almacenas el nombre de usuario en la sesión
            session['email_usuario'] = usuario_valido.Correo
            return redirect(url_for('tareas'))
        else:
            mensaje_error = "Usuario o contraseña incorrectos"

    return render_template('inicio.html', mensaje_error=mensaje_error)


@app.route('/crear-usuario', methods=['POST'])
def crear_usuario():
    # Verifica si el usuario está en la sesión
    if 'usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    usuario_actual = session['usuario']
    print(usuario_actual)
    jefe_obj = db_session.query(Jefe).filter_by(Usuario=usuario_actual).first()

    # Verificar si el usuario actual existe y tiene el cargo de 'Gerente'
    if jefe_obj is None or not es_gerente(jefe_obj):
        return jsonify({'error': 'Acción no permitida'}), 403

    # Extraer los datos del formulario desde request.form
    nombres = request.form['nombres']
    telefono = request.form['telefono']
    correo = request.form['correo']
    nombre_usuario = request.form['usuario']
    contrasena = request.form['contrasena']  # Asegúrate de usar hashing aquí en la práctica real

    # Crear una nueva instancia de Usuario
    nuevo_usuario = Usuario(
        Nombres=nombres,
        Telefono=telefono,
        Correo=correo,
        Usuario=nombre_usuario,
        Contraseña=contrasena  # Debería ser un hash seguro, no texto plano
    )

    try:
        db_session.add(nuevo_usuario)
        db_session.commit()
        return jsonify({'mensaje': 'Usuario creado con éxito'}), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500
    

# Función para verificar si el usuario es gerente
def es_gerente(usuario):
    return usuario.Cargo == 'Gerente'


@app.route('/inicio/jefe', methods=['GET', 'POST'])
def inicio_jefe():
    mensaje_error = ""
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        # Consulta la base de datos para verificar las credenciales
        jefe_valido = db_session.query(Jefe).filter_by(Usuario=usuario, Contraseña=contraseña).first()

        if jefe_valido:
            session['usuario_jefe'] = usuario
            session['email'] = jefe_valido.Correo
            #return redirect(url_for('creacion_usuarios'))
            return redirect(url_for('datos', pagina=1))
        else:
            mensaje_error = "Usuario o contraseña incorrectos"

    return render_template('jefe.html', mensaje_error=mensaje_error)


@app.route('/creacion', methods=['POST'])
def crear_tarea():
    if request.method == 'POST':
        creador = request.form['creador']
        contenido = request.form['contenido']
        usuario_designado = request.form['usuario_designado']  # Captura el ID del usuario designado
        dificultad = request.form['dificultad']  # Asume que hay un campo 'dificultad' en tu formulario
        fecha_creacion = datetime.strptime(request.form['fecha_creacion'], '%Y-%m-%d')

        nueva_tarea = Tareas(
            Creador=creador,
            Contenido=contenido,
            Designado=usuario_designado,  # Asigna el ID del usuario designado
            Dificultad=dificultad,  # Asigna la dificultad de la tarea
            creacion=fecha_creacion,
            Realizado=False,
            EnProgreso=False
        )

        db_session.add(nueva_tarea)
        db_session.commit()

        return redirect(url_for('tareas'))
    return render_template('creacion_tareas.html')  # Asegúrate de manejar esto adecuadamente

@app.route('/tareas')
def tareas():
    if 'usuario' not in session:
        return redirect(url_for('inicio'))

    usuario_actual = session['usuario']

    usuario_obj = db_session.query(Usuario).filter_by(Usuario=usuario_actual).first()
    if usuario_obj is None:
        return redirect(url_for('logout'))

    usuario_id = usuario_obj.Id

    tareas_no_realizadas = db_session.query(Tareas).filter_by(Realizado=False, EnProgreso=False, Designado=usuario_id).all()
    tareas_en_progreso = db_session.query(Tareas).filter_by(EnProgreso=True, Designado=usuario_id).all()
    tareas_realizadas = db_session.query(Tareas).filter_by(Realizado=True, Designado=usuario_id).all()

    # En lugar de renderizar la plantilla aquí, redireccionamos a la ruta '/datos/1'
    return redirect(url_for('datos_usuario', pagina=1))

def obtener_datos():
    datos = db_session.query(DataSynLab).all()
    for dato in datos:
        dato.Ticket = int(dato.Ticket)
        dato.Id_Solicitante = int(dato.Id_Solicitante)
    return datos

def obtener_datos2():
    datos = db_session.query(DataSynLab).filter(DataSynLab.Mail_Solicitante == session['email_usuario']).all()
    for dato in datos:
        dato.Ticket = int(dato.Ticket)
        dato.Id_Solicitante = int(dato.Id_Solicitante)
    return datos

@app.route('/datos/<int:pagina>')
def datos(pagina):
    todos_los_datos = obtener_datos()
    tamaño_pagina = 100
    total_datos = len(todos_los_datos)
    total_paginas = (total_datos + tamaño_pagina - 1) // tamaño_pagina  # Redondea hacia arriba
    inicio = (pagina - 1) * tamaño_pagina
    fin = inicio + tamaño_pagina
    # Si se solicita una página que no existe, redirigir a la última página disponible
    if inicio >= total_datos:
        return redirect(url_for('datos', pagina=total_paginas))
    datos_paginados = todos_los_datos[inicio:fin]
    
    # Asegúrate de que 'tu_plantilla.html' maneja 'datos_paginados', 'pagina', y 'total_paginas' correctamente.
    return render_template('tu_plantilla.html', datos_paginados=datos_paginados, pagina=pagina, total_paginas=total_paginas)


@app.route('/datospp/<int:pagina>')
def datos_usuario(pagina):
    todos_los_datos = obtener_datos2()
    tamaño_pagina = 100
    total_datos = len(todos_los_datos)
    total_paginas = (total_datos + tamaño_pagina - 1) // tamaño_pagina  # Redondea hacia arriba
    inicio = (pagina - 1) * tamaño_pagina
    fin = inicio + tamaño_pagina
    # Si se solicita una página que no existe, redirigir a la última página disponible
    if inicio >= total_datos:
        return redirect(url_for('datospp', pagina=total_paginas))
    datos_paginados = todos_los_datos[inicio:fin]
    
    # Asegúrate de que 'tu_plantilla.html' maneja 'datos_paginados', 'pagina', y 'total_paginas' correctamente.
    return render_template('tu_plantilla2.html', datos_paginados=datos_paginados, pagina=pagina, total_paginas=total_paginas)

# Si decides mantener esta ruta, asegúrate de que su uso esté justificado.
@app.route('/datos-synlab')
def datos_synlab():
    # Esta ruta podría ser utilizada para una vista resumen o algo especial.
    # Si no, es mejor quitarla o modificarla para que no recupere todos los datos sin paginar.
    datos = db_session.query(DataSynLab).all()
    return render_template('tablas.html', datos=datos)


@app.route('/api/predecir-prioridad', methods=['POST'])
def predecir_prioridad():
    # Obtener el texto del cuerpo de la solicitud
    datos = request.get_json()
    texto = datos['text']

    # Convertir ese texto en un formato que el modelo pueda entender
    df = pd.DataFrame([texto], columns=['text'])

    # Realizar la predicción
    resultado_prediccion = modelo.predict(df)

    # Convertir el resultado de numpy int64 a int nativo de Python para JSON
    resultado_prediccion = int(resultado_prediccion[0])

    # Devolver la prioridad predicha como respuesta JSON
    return jsonify({'prioridad': resultado_prediccion})


@app.route('/creacion_tareas')
def creacion_tareas():
    usuarios = db_session.query(Usuario).all()
    resultados_json = json.dumps([])  # cadena JSON vacía para evitar errores
    return render_template('creacion_tareas.html', usuarios=usuarios, resultados_json=resultados_json)


@app.route('/creacion_usuarios')
def creacion_usuarios():
    usuarios = db_session.query(Usuario).all()
    resultados_json = json.dumps([])  # cadena JSON vacía para evitar errores
    return render_template('creacion_usuarios.html', usuarios=usuarios, resultados_json=resultados_json)


@app.route('/logout', methods=['POST'])
def logout():
    # Elimina el nombre de usuario de la sesión si está presente
    session.pop('usuario', None)
    # Redirige al usuario a la página de inicio o a la página que desees después del deslogueo
    return redirect(url_for('inicio'))


# @app.route('/prediccion', methods=['POST'])
# def prediccion():
#     dificultad_valores = case([
#         (Tareas.Dificultad == 'Bajo', 40),
#         (Tareas.Dificultad == 'Medio', 45),
#         ], else_=50)

#     tareas_pendientes = db_session.query(Tareas, dificultad_valores.label("Dificultad_numerica")).filter(Tareas.Realizado == False).all()

#     cantidad_tareas = db_session.query(Tareas).filter(Tareas.EnProgreso == True).count()

#     # Cambio en la consulta de duracion_promedio
#     stmt = text("SELECT AVG(DATEDIFF(MINUTE, creacion, fecha_termino)) FROM Tareas WHERE Realizado = 1")
#     promedio_minutos = db_session.execute(stmt).scalar()

#     resultados = []

#     for tarea, dificultad_num in tareas_pendientes:
#         X = [[0.75, dificultad_num, promedio_minutos, 0, tarea.NUMERO_TRABAJADORES]]

#         prediction = model.predict(X)
#         resultados.append({
#             'Tarea_Id': tarea.Id,
#             'Contenido': tarea.Contenido,
#             'Prediccion': str(prediction[0][0])
#         })

#     resultados_json = json.dumps(resultados)

#     # Decodificar la cadena JSON a un objeto Python
#     resultados_obj = json.loads(resultados_json)

#     return render_template('creacion_tareas.html', resultados_json=resultados)


@app.route('/tarea/<int:tarea_id>')
def detalle_tarea(tarea_id):
    # Obtener detalles de la tarea de la base de datos
    tarea = db_session.query(Tareas).filter_by(Id=tarea_id).first()
    if tarea is None:
        # Si no se encuentra la tarea, redirige o muestra un error
        return "Tarea no encontrada", 404
    return render_template('detalle.html', tarea=tarea)