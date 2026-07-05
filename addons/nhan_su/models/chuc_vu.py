from odoo import fields, models


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Chức vụ'
    _rec_name = 'ten_chuc_vu'
    _order = 'ma_chuc_vu asc'

    ma_chuc_vu = fields.Char('Mã chức vụ', required=True)
    ten_chuc_vu = fields.Char('Tên chức vụ', required=True)
    mo_ta = fields.Text('Mô tả')

    _sql_constraints = [
        ('ma_chuc_vu_unique', 'unique(ma_chuc_vu)', 'Mã chức vụ phải là duy nhất.'),
    ]
