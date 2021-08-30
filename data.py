
from app.auth import login_required
from flask_login import login_user, logout_user, login_required, current_user
import functools
import copy
from sqlalchemy import *
from datetime import datetime, date, time, timedelta
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

    today = date.today()
    start_date = today + timedelta(days= (7 - today.weekday()))
    end_date = start_date + timedelta(days=6)

    context['fecha_inicio'] = copy.copy(start_date)
    context['fecha_fin'] = copy.copy(end_date)

    if request.method == 'POST':
        delta = timedelta(days=1)
        hay_fechas = Dia_comida.query.filter_by(fecha=start_date).first()
        relacion_dias_fechas = {}
        index=0
        while start_date <= end_date:  
            if hay_fechas is None:        
                registro_dias = Dia_comida(fecha=start_date)
                db.session.add(registro_dias)
                db.session.commit()

            relacion_dias_fechas[dias[index][0]] = start_date

            start_date += delta
            index += 1
        
        start_date2 = today + timedelta(days= (7 - today.weekday()))
        fechas_proxima_semana = Dia_comida.query.filter(Dia_comida.fecha.between(start_date2, end_date)).all()
        tiene_reserva = Reserva_comida.query.filter(and_(Reserva_comida.id_dia_comida>=fechas_proxima_semana[0].id, Reserva_comida.id_dia_comida<=fechas_proxima_semana[6].id, Reserva_comida.id_user==current_user.id)).first()

        if tiene_reserva:
            flash('Usted ya ha reservado para esta semana.', category='error')
        else:
            turnos = Turno.query.all()
            check_reservas_guardadas = False
            for turno in turnos:
                for dia in dias:
                    turno_dia = (turno.tipo_turno + '_' + dia[0])
                    if turno_dia in request.form:
                        recibido = request.form[turno_dia] 
                        if recibido:
                            id_turno = Turno.query.filter_by(tipo_turno=turno.tipo_turno).first()
                            fecha_elegida = relacion_dias_fechas[dia[0]]
                            id_dia = Dia_comida.query.filter_by(fecha=fecha_elegida).first()
                            reserva_comida = Reserva_comida(id_user=current_user.id, id_turno=id_turno.id, id_dia_comida=id_dia.id)
                            db.session.add(reserva_comida)
                            check_reservas_guardadas = True

            if check_reservas_guardadas:              
                db.session.commit()
                flash('Reserva realizada.', category='success')
            else:
                flash('No has seleccionado nada.', category='error')
    
    if date.today().weekday() <= 2: 
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
            except:
                raise Exception('Ha ocurrido un error al guardar la reserva de deporte.')
        else:
            flash('No hay plazas libres para esa fecha.', category='error')
        
    return render_template('content/deporte.html', user=current_user)
