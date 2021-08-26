
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

    # Falta sacar las fechas de cada dia de la semana que viene en 'fechas'

    today = date.today()
    start_date = today + timedelta(days= (7 - today.weekday()))
    end_date = start_date + timedelta(days=7)
    delta = timedelta(days=1)

    if request.method == 'POST':

        es_nuevo = query(start_date)
          
        relacion_dias_fechas = {}
        index=0
        while start_date <= end_date:
            if es_nuevo:        
                registro_dias = Dia_comida(fecha=start_date)
                db.session.add(registro_dias)
                

            relacion_dias_fechas[dias[index][0]] = start_date
            start_date += delta
            index += 1

        if es_nuevo:
            db.session.commit()
    
        raise Exception('Ha ocurrido un error al crear los días de comida.')


        
        
        reserva = []
        for kdia, dia in dias:

            reserva.append(kdia)
        

        # c.execute(
        #     'select id from dia_comida where fecha = %s', (now.date(),)
        # )
        # id_dia_comida = c.fetchone()
        # c.execute(
        #     """
        #     insert into turno ( 
        #         tipo_turno,
        #         id_dia_comida
        #     )
        #     values 
        #         ('desayuno', %s),
        #         ('comida', %s),
        #         ('cena', %s);
        #     """, (id_dia_comida, id_dia_comida, id_dia_comida)
        # )
        # db.commit()

        return redirect(url_for('main.menu'))
    
    if date.today().weekday() <= 2:
        return render_template('content/apuntarse.html', user=current_user, dias = dias, turnos = turnos)

        context = {'user':current_user, 'dias' : dias, 'turnos' : turnos}
        return render_template('content/apuntarse.html', context=context) 
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
