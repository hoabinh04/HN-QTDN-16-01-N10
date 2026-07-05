from odoo import fields, models


class DonVi(models.Model):
    _name = 'don_vi'
    _description = 'Đơn vị'
    _rec_name = 'ten_don_vi'
    _order = 'ma_don_vi asc'

    ma_don_vi = fields.Char('Mã đơn vị', required=True)
    ten_don_vi = fields.Char('Tên đơn vị', required=True)
    don_vi_cha_id = fields.Many2one('don_vi', string='Đơn vị cấp trên', ondelete='restrict')
    mo_ta = fields.Text('Mô tả')
    nhan_vien_ids = fields.One2many('nhan_vien', 'don_vi_hien_tai_id', string='Nhân viên hiện tại')
    so_luong_nhan_vien = fields.Integer('Số nhân viên', compute='_compute_so_luong_nhan_vien')

    _sql_constraints = [
        ('ma_don_vi_unique', 'unique(ma_don_vi)', 'Mã đơn vị phải là duy nhất.'),
    ]

    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_ids)
