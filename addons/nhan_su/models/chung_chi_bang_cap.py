from odoo import fields, models


class ChungChiBangCap(models.Model):
    _name = 'chung_chi_bang_cap'
    _description = 'Chứng chỉ/Bằng cấp'
    _rec_name = 'ten_chung_chi_bang_cap'
    _order = 'ma_chung_chi_bang_cap asc'

    ma_chung_chi_bang_cap = fields.Char('Mã chứng chỉ/bằng cấp', required=True)
    ten_chung_chi_bang_cap = fields.Char('Tên chứng chỉ/bằng cấp', required=True)
    nhom = fields.Selection(
        [
            ('degree', 'Bằng cấp'),
            ('certificate', 'Chứng chỉ'),
            ('skill', 'Kỹ năng'),
            ('other', 'Khác'),
        ],
        string='Nhóm',
        default='certificate',
        required=True,
    )
    mo_ta = fields.Text('Mô tả')

    _sql_constraints = [
        (
            'ma_chung_chi_bang_cap_unique',
            'unique(ma_chung_chi_bang_cap)',
            'Mã chứng chỉ/bằng cấp phải là duy nhất.',
        ),
    ]
