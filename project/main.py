# -*- coding:utf-8 -*-
from datetime import datetime
from pytz import timezone
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


from project import db
from project.forms import CreateWorkForm, CreateStaffPersonalForm
from project.models import PerformanceAgreement, StaffPersonalInfo

main = Blueprint('main', __name__)
bangkok = timezone('Asia/Bangkok')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/performance_agreement/year')
@login_required
def show_year():
    return render_template('assessment_round.html')


@main.route('/performance_agreement/report')
def report_info():
    staff_info = StaffPersonalInfo.query.all()
    return render_template('report_info.html', staff_info=staff_info)


@main.route('/performance_agreement/personal/add', methods=['GET', 'POST'])
@login_required
def add_staff():
    form = CreateStaffPersonalForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            staff = StaffPersonalInfo()
            form.populate_obj(staff)
            db.session.add(staff)
            db.session.commit()
            flash(u'บันทึกข้อมูลเรียบร้อย', 'success')
            # return redirect(url_for('main.show_personal_info'))
        else:
            print(form.errors)
            flash(u'ข้อมูลไม่ถูกต้อง กรุณาตรวจสอบ', 'danger')
    return render_template('add_staff.html', form=form)


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


