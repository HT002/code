
from app.auth import login_required

import functools


from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.utils import redirect

from app.db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/comida', methods=['GET', 'POST'])
@login_required
def comida():
    if request.method == 'POST':
        L1 = request.form['L1']
        L2 = request.form['L2']
        L3 = request.form['L3']
        M1 = request.form['M1']
        M2 = request.form['M2']
        M3 = request.form['M3']
        X1 = request.form['X1']
        X2 = request.form['X2']
        X3 = request.form['X3']
        J1 = request.form['J1']
        J2 = request.form['J2']
        J3 = request.form['J3']
        V1 = request.form['V1']
        V2 = request.form['V2']
        V3 = request.form['V3']
        S1 = request.form['S1']
        S2 = request.form['S2']
        S3 = request.form['S3']
        D1 = request.form['D1']
        D2 = request.form['D2']
        D3 = request.form['D3']
        usuario = request.form['usuario']

        db, c = get_db()
        error = None
        c.execute(
            'select tim from user where username = %s', (usuario,)
        )
        tim = c.fetchone()

        c.execute(
            'insert into comida (tim, L1, L2, L3, M1, M2, M3, X1, X2, X3, J1, J2, J3, V1, V2, V3, S1, S2, S3, D1, D2, D3) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (str(tim), str(L1), str(L2), str(L3), str(M1), str(M2), str(M3), str(X1), str(X2), str(X3), str(J1), str(J2), str(J3), str(V1), str(V2), str(V3), str(S1), str(S2), str(S3), str(D1), str(D2), str(D3))
        )
        db.commit()

        return redirect(url_for('main.menu'))
    
    return render_template('content/apuntarse.html')


@bp.route('/deporte', methods=['GET', 'POST'])
@login_required
def deporte():
    if request.method == 'POST':
        fecha = request.form['fecha']
        deporte = request.form['deporte']
        db, c = get_db()
        error = None

        c.execute(
            """
            select 
                z.id as id_zona, 
                d.id as id_deporte
            from deporte d 
            inner join zona z on z.id_deporte = d.id
            where 
                d.identificador_deporte = '%s' 
                and z.id not in (
                    select rd.id_zona
                    from reserva_deporte rd
                    where rd.fecha = '%s'
                )
            """, (deporte, fecha)
        )
        reservas_disponibles = c.fetchone()
        if reservas_disponibles is None:
            error = 'Esa hora ya ha sido reservada.'
        else:

            return redirect(url_for('main.index'))
    
        flash(error)

    return render_template('content/deporte.html')
