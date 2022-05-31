# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory, QuerySelectField

from . import db
from .models import PerformanceAgreement, StaffPosition

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


# Create a Form Class
class CreateWorkForm(ModelForm):
    class Meta:
        model = PerformanceAgreement

    position = QuerySelectField(query_factory=lambda: StaffPosition.query.all(),
                                 get_label='fullname_th',
                                 label=u'ตำแหน่ง')
    job_desc = QuerySelectField(query_factory=lambda: StaffPosition.query.all(),
                                get_label='job_desc',
                                label=u'หน้าที่และความรับผิดชอบ')


