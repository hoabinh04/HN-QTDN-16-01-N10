from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DanhSachChungChiBangCap(models.Model):
    _name = 'danh_sach_chung_chi_bang_cap'
    _description = 'Chứng chỉ/Bằng cấp của nhân viên'
    _rec_name = 'ten_hien_thi'
    _order = 'ngay_cap desc, id desc'

    ten_hien_thi = fields.Char('Tên hiển thị', compute='_compute_ten_hien_thi', store=True)
    chung_chi_bang_cap_id = fields.Many2one(
        'chung_chi_bang_cap',
        string='Chứng chỉ/Bằng cấp',
        required=True,
    )
    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    ma_dinh_danh = fields.Char('Mã nhân viên', related='nhan_vien_id.ma_dinh_danh', store=True)
    tuoi = fields.Integer('Tuổi', related='nhan_vien_id.tuoi')
    so_hieu = fields.Char('Số hiệu')
    noi_cap = fields.Char('Nơi cấp')
    ngay_cap = fields.Date('Ngày cấp')
    ngay_het_han = fields.Date('Ngày hết hạn')
    tep_dinh_kem = fields.Binary('Tệp đính kèm', attachment=True)
    ten_tep = fields.Char('Tên tệp')
    trang_thai = fields.Selection(
        [
            ('valid', 'Còn hiệu lực'),
            ('expired', 'Hết hiệu lực'),
            ('unknown', 'Chưa xác định'),
        ],
        string='Trạng thái',
        compute='_compute_trang_thai',
        store=True,
    )
    ghi_chu = fields.Char('Ghi chú')

    @api.depends('nhan_vien_id', 'chung_chi_bang_cap_id')
    def _compute_ten_hien_thi(self):
        for record in self:
            parts = [record.nhan_vien_id.ho_va_ten, record.chung_chi_bang_cap_id.ten_chung_chi_bang_cap]
            record.ten_hien_thi = ' - '.join(part for part in parts if part)

    @api.depends('ngay_het_han')
    def _compute_trang_thai(self):
        today = fields.Date.context_today(self)
        for record in self:
            if not record.ngay_het_han:
                record.trang_thai = 'unknown'
            elif record.ngay_het_han < today:
                record.trang_thai = 'expired'
            else:
                record.trang_thai = 'valid'

    @api.constrains('ngay_cap', 'ngay_het_han')
    def _check_thoi_han(self):
        for record in self:
            if record.ngay_cap and record.ngay_het_han and record.ngay_het_han < record.ngay_cap:
                raise ValidationError('Ngày hết hạn không được nhỏ hơn ngày cấp.')
