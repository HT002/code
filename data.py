
from app.auth import login_required
from flask_login import login_user, logout_user, login_required, current_user
import functools
from datetime import datetime
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
    if request.method == 'POST':
        now = datetime.now()

        c.execute(
            'select id from dia_comida where fecha = %s', (now.date(),)
        )
        id_dia_comida = c.fetchone()
        c.execute(
            """
            insert into turno ( 
                tipo_turno,
                id_dia_comida
            )
            values 
                ('desayuno', %s),
                ('comida', %s),
                ('cena', %s);
            """, (id_dia_comida, id_dia_comida, id_dia_comida)
        )
        db.commit()

        return redirect(url_for('main.menu'))
    
    return render_template('content/apuntarse.html', user=current_user)


@bp.route('/deporte', methods=['GET', 'POST'])
@login_required
def deporte():
    if request.method == 'POST':
        fecha = request.form['fecha']
        deporte_id = request.form['deporte']
        deporte = Deporte.query.filter(Deporte.identificador_deporte==deporte_id).first()
        reservas_en_fecha = Reserva_deporte.query.filter(Reserva_deporte.fecha==fecha).all()
        ids_zona_reservada = []
        for ref in reservas_en_fecha:
            ids_zona_reservada.append(ref.id_zona)
        
        zona_libre = Zona.query.filter(Zona.id_deporte==deporte.id).filter(Zona.id not in ids_zona_reservada).first()

        if fecha:
            reserva_deporte = Reserva_deporte(fecha=fecha, id_user=current_user.id, id_zona=zona_libre.id)
            # reserva_deporte.save()
            try:
                db.session.add(reserva_deporte)
                db.session.commit()
            except:
                raise Exception("Ha ocurrido un error al guardar la reserva de deporte")

        # c.execute(
        #     """
        #     select 
        #         z.id as id_zona
        #     from deporte d 
        #     inner join zona z on z.id_deporte = d.id
        #     where 
        #         d.identificador_deporte = %s 
        #         and z.id not in (
        #             select rd.id_zona
        #             from reserva_deporte rd
        #             where rd.fecha = %s
        #         )
        #     """, (deporte, fecha)
        # )


    return render_template('content/deporte.html', user=current_user)
