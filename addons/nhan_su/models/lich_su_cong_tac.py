from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LichSuCongTac(models.Model):
    _name = 'lich_su_cong_tac'
    _description = 'Lịch sử công tác'
    _rec_name = 'ten_lich_su'
    _order = 'ngay_bat_dau desc, id desc'

    ten_lich_su = fields.Char('Tên lịch sử', compute='_compute_ten_lich_su', store=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    chuc_vu_id = fields.Many2one('chuc_vu', string='Chức vụ', required=True)
    don_vi_id = fields.Many2one('don_vi', string='Đơn vị', required=True)
    loai_chuc_vu = fields.Selection(
        [
            ('main', 'Chính'),
            ('concurrent', 'Kiêm nhiệm'),
        ],
        string='Loại chức vụ',
        default='main',
        required=True,
    )
    ngay_bat_dau = fields.Date('Ngày bắt đầu', required=True)
    ngay_ket_thuc = fields.Date('Ngày kết thúc')
    dang_hieu_luc = fields.Boolean('Đang hiệu lực', compute='_compute_dang_hieu_luc', store=True)
    ghi_chu = fields.Text('Ghi chú')

    @api.depends('nhan_vien_id', 'chuc_vu_id', 'don_vi_id')
    def _compute_ten_lich_su(self):
        for record in self:
            parts = [record.nhan_vien_id.ho_va_ten, record.chuc_vu_id.ten_chuc_vu, record.don_vi_id.ten_don_vi]
            record.ten_lich_su = ' - '.join(part for part in parts if part)

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_dang_hieu_luc(self):
        today = fields.Date.context_today(self)
        for record in self:
            record.dang_hieu_luc = bool(
                record.ngay_bat_dau
                and record.ngay_bat_dau <= today
                and (not record.ngay_ket_thuc or record.ngay_ket_thuc >= today)
            )

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_thoi_gian_cong_tac(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc and record.ngay_ket_thuc < record.ngay_bat_dau:
                raise ValidationError('Ngày kết thúc công tác không được nhỏ hơn ngày bắt đầu.')
