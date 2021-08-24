
from app.auth import login_required
import functools
from datetime import datetime
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.utils import redirect

from sqlalchemy import *
from . import db
from .models import Deporte, Zona, Reserva_deporte, Dia_comida, Turno, Reserva_comida, User

from .schema_menu import orders

bp = Blueprint('data', __name__, url_prefix='/data')

def create_menu():
    db, c = get_db()

    for i in orders:
        c.execute(i)

    db.commit()

@bp.route('/comida', methods=['GET', 'POST'])
@login_required
def comida():
    if request.method == 'POST':
        now = datetime.now()
        error = None

        create_menu()
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
    
    return render_template('content/apuntarse.html')


@bp.route('/deporte', methods=['GET', 'POST'])
@login_required
def deporte():
    if request.method == 'POST':
        user_id = g.user.id
        fecha = request.form['fecha']
        deporte = request.form['deporte']

        new_user = Reserva_deporte(id=56, fecha=fecha, id_user=user_id, id_zona=56)
        db.session.add(new_user)
        db.session.commit()


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


    return render_template('content/deporte.html')
