# -*- coding:utf-8 -*-
from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms_alchemy import model_form_factory

from . import db

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String(), unique=True)
    password = db.Column('password', db.String())
    name = db.Column('name', db.String())


# Create db organization model
class Org(db.Model):
    __tablename__ = 'orgs'
    id = db.Column('id', db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': u'ชื่อหน่วยงาน/องค์กร/ภาควิชา(TH)'})
    en_name = db.Column('en_name', db.String(), info={'label': u'ชื่อหน่วยงาน/องค์กร/ภาควิชา(EN)'})
    head = db.Column('head', db.String(), info={'label': u'หัวหน้า'})
    parent_id = db.Column('parent_id', db.Integer, db.ForeignKey('orgs.id'))
    children = db.relationship('Org', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return '<Name %r>' % self.name
    # def __repr__(self):
    #     return self.name


# Create db staff model
class StaffPersonalInfo(db.Model):
    __tablename__ = 'staff_personal_info'
    id = db.Column('id', db.Integer(), primary_key=True, autoincrement=True)
    th_title = db.Column('th_title', db.String(), info={'label': u'คำนำหน้า(TH)'})
    th_firstname = db.Column('th_firstname', db.String(), info={'label': u'ชื่อ(TH)'})
    th_lastname = db.Column('th_lastname', db.String(), info={'label': u'นามสกุล(TH)'})
    en_title = db.Column('en_title', db.String(), info={'label': u'คำนำหน้า(EN)'})
    en_firstname = db.Column('en_firstname', db.String(), info={'label': u'ชื่อ(EN)'})
    en_lastname = db.Column('en_lastname', db.String(), info={'label': u'นามสกุล(EN)'})
    org_id = db.Column('orgs_id', db.ForeignKey('orgs.id'))
    org = db.relationship(Org, backref=db.backref('staff'))
    employed_date = db.Column('employed_date', db.Date(), info={'label': u'วันที่เริ่มงาน'})
    employment_id = db.Column('employment_id',
                              db.ForeignKey('staff_employments.id'))
    employment = db.relationship('StaffEmployment',
                                 backref=db.backref('staff'))

    def __repr__(self):
        return '<FullName %r>' % self.fullname

    # def __str__(self):
    #     return self.fullname

    @property
    def fullname(self):
        if self.th_firstname or self.th_lastname:
            return u'{}{} {}'.format(self.th_title or u'คุณ', self.th_firstname, self.th_lastname)
        else:
            return u'{}{} {}'.format(self.en_title or '', self.en_firstname, self.en_lastname)


class StaffPosition(db.Model):
    __tablename__ = 'staff_position'
    id = db.Column('id', db.Integer(), primary_key=True, autoincrement=True)
    fullname_th = db.Column('fullname_th', db.String(), nullable=False, info={'label': u'ตำแหน่ง(TH)'})
    fullname_en = db.Column('fullname_en', db.String(), info={'label': u'ตำแหน่ง(EN)'})
    job_desc = db.Column('job_desc', db.Text(), info={'label': u'หน้าที่และความรับผิดชอบ'})
    type = db.Column('type', db.String(), info={'label': u'ตำแหน่งประเภท',
                                                'choices': [(c, c) for c in [u'ประเภทสนับสนุน', u'ประเภทวิชาการ',
                                                                             u'ประเภทผู้บริหาร(ระดับต้นและระดับกลาง)',
                                                                             u'ประเภทผู้บริหารอื่นๆ']]})

    def __repr__(self):
        return '<FullnameTH %r>' % self.fullname_th


class StaffEmployment(db.Model):
    __tablename__ = 'staff_employments'
    id = db.Column('id', db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(), unique=True, nullable=False)

    def __repr__(self):
        return '<Title %r>' % self.title
    # def __str__(self):
    #     return self.title


# Create db Performance Agreement model
class PerformanceAgreement(db.Model):
    __tablename__ = 'performance_agreements'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    work = db.Column('work', db.String(), nullable=False, info={'label': u'ภาระงาน'})
    details = db.Column('details', db.Text(), info={'label': u'รายละเอียด'})
    personal_id = db.Column('personal_id', db.ForeignKey('staff_personal_info.id'))
    personal_info = db.relationship("StaffPersonalInfo")
    appraisal_cycle = db.Column('appraisal_cycle', db.String(), info={'label': u'รอบประเมิน'})
    percentage = db.Column('percentage', db.Float(), info={'label': u'ร้อยละน้ำหนัก'})
    start_date = db.Column('start_date', db.Date(), info={'label': u'วันที่เริ่มประเมิน'})
    end_date = db.Column('end_date', db.Date(), info={'label': u'ประเมินถึงวันที่'})
    comment = db.Column('comment', db.Text(), info={'label': u'หมายเหตุ'})
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # def __str__(self):
    #     return u'{}'.format(self.work)
    # Create A String
    def __repr__(self):
        return '<Work %r>' % self.work