# -*- coding:utf-8 -*-
from datetime import datetime
from pytz import timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


from project import db
from project.forms import CreateWorkForm
from project.models import PerformanceAgreement

main = Blueprint('main', __name__)
bangkok = timezone('Asia/Bangkok')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/project/create', methods=['POST', 'GET'])
@login_required
def create_work():
    form = CreateWorkForm()
    if request.method == 'POST':
        work = PerformanceAgreement()
        form.populate_obj(work)
        work.updated_at = bangkok.localize(datetime.now())
        try:
            db.session.add(work)
            db.session.commit()
            flash(u'บันทึกข้อมูลสำเร็จ.', 'success')
            return redirect(url_for('performance_agreement.create_work'))
        except:
            # Check Error
            for er in form.errors:
                flash(er, 'danger')
    else:
        works = PerformanceAgreement.query.order_by(PerformanceAgreement.updated_at)
        return render_template('create_work.html', form=form, works=works)

