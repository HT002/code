
from app.auth import login_required
from flask_login import login_user, logout_user, login_required, current_user
import functools
from datetime import datetime, date, timedelta
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from . import db
from .models import Deporte, Zona, Reserva_deporte, Dia_comida, Turno, Reserva_comida, User

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/comida', methods=['GET', 'POST'])
@login_required
def comida():
    dias = [('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miercoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sabado'), ('domingo', 'Domingo')]
    turnos = [('desayuno', 'Desayuno'), ('comida', 'Comida'), ('cena', 'Cena')]
    context = {'dias': dias, 'turnos': turnos}

    if request.method == 'POST':
        context = context
        today = date.today()
        start_date = today + timedelta(days= (7 - today.weekday()))
        end_date = start_date + timedelta(days=7)
        delta = timedelta(days=1)
        hay_fechas = Dia_comida.query.filter_by(fecha=start_date).first()
        relacion_dias_fechas = {}
        index=0

        while start_date <= end_date:  
            if hay_fechas is None:        
                registro_dias = Dia_comida(fecha=start_date)
                db.session.add(registro_dias)
                db.session.commit()
            
            relacion_dias_fechas[context['dias'][index][0]] = start_date
            start_date += delta
            index += 1
        
        # Lo he hecho respecto a esto: puedo meter un identificador_dia en Dia_comida para no necesitar la relacion_dias_fechas y buscar por el nombre del dia.
        # ¿O es información que sobra en la base de datos pudiendo hacerlo aquí?

        # raise Exception(relacion_dias_fechas) ## me dice: IndexError: list index out of range
    
        turnos = Turno.query(Turno.id, Turno.tipo_turno)
        fechas = Dia_comida.query(Dia_comida.id, Dia_comida.fecha)
        index2 = 0

        for t in turnos.tipo_turno:
            for d in context['dias'][index2][0]:
                index2 += 1
                turno_dia = (t + '_' + d)
                recibido = request.form[turno_dia]
                if recibido:
                    recibido_separado = recibido.split('_')
                    id_turno = Turno.query.filter_by(tipo_turno=recibido_separado[0]).first()
                    id_dia = Dia_comida.query.filter_by(identificador_dia=recibido_separado[1]).first()
                    reserva_comida = Reserva_comida(id_user=current_user.id, id_turno=id_turno.id, id_dia_comida=id_dia.id)
                    db.session.add(reserva_comida)
                    db.session.commit()
                    flash('Reserva realizada.', category='success')

        return redirect(url_for('main.menu'))
    
    if date.today().weekday() <= 5: #Hay que poner un 2. El 5 es para las pruebas
        return render_template('content/apuntarse.html', user=current_user, context=context) 
    else:
        return render_template('content/reserva_cerrada.html', user=current_user)


@bp.route('/deporte', methods=['GET', 'POST'])
@login_required
def deporte():
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            deporte = request.form['deporte']
            deporte_id = Deporte.query.filter(Deporte.identificador_deporte==deporte).first()
            reservas_en_fecha = Reserva_deporte.query.filter(Reserva_deporte.fecha==fecha).all()
            ids_zona_reservada = []
            for ref in reservas_en_fecha:
                ids_zona_reservada.append(ref.id_zona)
            zona_libre = Zona.query.filter(Zona.id_deporte==deporte_id.id).filter(not_(Zona.id.in_(ids_zona_reservada))).first()
        except:
            raise Exception("Ha ocurrido un error al recibir los datos de deporte.")
        
        if zona_libre:
            reserva_deporte = Reserva_deporte(fecha=fecha, id_user=current_user.id, id_zona=zona_libre.id)
            try:
                db.session.add(reserva_deporte)
                db.session.commit()
                flash('Reserva realizada.', category='success')
            except Exception as e:
                raise Exception('Ha ocurrido un error al guardar la reserva de deporte.')
        else:
            flash('No hay plazas libres para esa fecha.', category='error')
        
    return render_template('content/deporte.html', user=current_user)
