from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Hồ sơ nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'ten asc, ho_ten_dem asc'

    ma_dinh_danh = fields.Char('Mã nhân viên', required=True)
    ho_ten_dem = fields.Char('Họ tên đệm', required=True)
    ten = fields.Char('Tên', required=True)
    ho_va_ten = fields.Char('Họ và tên', compute='_compute_ho_va_ten', store=True)
    gioi_tinh = fields.Selection(
        [
            ('male', 'Nam'),
            ('female', 'Nữ'),
            ('other', 'Khác'),
        ],
        string='Giới tính',
    )
    ngay_sinh = fields.Date('Ngày sinh')
    tuoi = fields.Integer('Tuổi', compute='_compute_tuoi', store=True)
    so_cccd = fields.Char('Số CCCD/CMND')
    ngay_cap_cccd = fields.Date('Ngày cấp')
    noi_cap_cccd = fields.Char('Nơi cấp')
    que_quan = fields.Char('Quê quán')
    dia_chi_lien_he = fields.Char('Địa chỉ liên hệ')
    email = fields.Char('Email')
    so_dien_thoai = fields.Char('Số điện thoại')
    ngay_vao_lam = fields.Date('Ngày vào làm')
    ngay_nghi_viec = fields.Date('Ngày nghỉ việc')
    trang_thai = fields.Selection(
        [
            ('draft', 'Hồ sơ mới'),
            ('working', 'Đang làm việc'),
            ('leave', 'Tạm nghỉ'),
            ('resigned', 'Đã nghỉ việc'),
        ],
        string='Trạng thái',
        default='working',
        required=True,
    )
    active = fields.Boolean('Đang theo dõi', default=True)
    anh = fields.Binary('Ảnh')
    ghi_chu = fields.Text('Ghi chú')
    lich_su_cong_tac_ids = fields.One2many(
        'lich_su_cong_tac',
        inverse_name='nhan_vien_id',
        string='Lịch sử công tác',
    )
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        'danh_sach_chung_chi_bang_cap',
        inverse_name='nhan_vien_id',
        string='Chứng chỉ/Bằng cấp',
    )
    don_vi_hien_tai_id = fields.Many2one(
        'don_vi',
        string='Đơn vị hiện tại',
        compute='_compute_cong_tac_hien_tai',
        store=True,
    )
    chuc_vu_hien_tai_id = fields.Many2one(
        'chuc_vu',
        string='Chức vụ hiện tại',
        compute='_compute_cong_tac_hien_tai',
        store=True,
    )
    so_nguoi_bang_tuoi = fields.Integer(
        'Số người bằng tuổi',
        compute='_compute_so_nguoi_bang_tuoi',
    )

    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã nhân viên phải là duy nhất.'),
        ('so_cccd_unique', 'unique(so_cccd)', 'Số CCCD/CMND phải là duy nhất.'),
    ]

    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_va_ten(self):
        for record in self:
            record.ho_va_ten = ' '.join(part for part in [record.ho_ten_dem, record.ten] if part)

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        today = date.today()
        for record in self:
            if record.ngay_sinh:
                born = record.ngay_sinh
                record.tuoi = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            else:
                record.tuoi = 0

    @api.depends('tuoi')
    def _compute_so_nguoi_bang_tuoi(self):
        for record in self:
            if not record.tuoi:
                record.so_nguoi_bang_tuoi = 0
                continue
            domain = [('tuoi', '=', record.tuoi)]
            if record.id:
                domain.append(('id', '!=', record.id))
            record.so_nguoi_bang_tuoi = self.search_count(domain)

    @api.depends(
        'lich_su_cong_tac_ids.ngay_bat_dau',
        'lich_su_cong_tac_ids.ngay_ket_thuc',
        'lich_su_cong_tac_ids.loai_chuc_vu',
        'lich_su_cong_tac_ids.don_vi_id',
        'lich_su_cong_tac_ids.chuc_vu_id',
    )
    def _compute_cong_tac_hien_tai(self):
        today = fields.Date.context_today(self)
        for record in self:
            current_jobs = record.lich_su_cong_tac_ids.filtered(
                lambda job: job.loai_chuc_vu == 'main'
                and job.ngay_bat_dau
                and job.ngay_bat_dau <= today
                and (not job.ngay_ket_thuc or job.ngay_ket_thuc >= today)
            ).sorted('ngay_bat_dau', reverse=True)
            current_job = current_jobs[:1]
            record.don_vi_hien_tai_id = current_job.don_vi_id if current_job else False
            record.chuc_vu_hien_tai_id = current_job.chuc_vu_id if current_job else False

    @api.onchange('ten', 'ho_ten_dem')
    def _default_ma_dinh_danh(self):
        for record in self:
            if not record.ma_dinh_danh and record.ho_ten_dem and record.ten:
                initials = ''.join(part[0] for part in record.ho_ten_dem.lower().split() if part)
                record.ma_dinh_danh = '%s%s' % (record.ten.lower(), initials)

    @api.constrains('tuoi', 'ngay_sinh')
    def _check_tuoi(self):
        for record in self:
            if record.ngay_sinh and record.tuoi < 18:
                raise ValidationError('Nhân viên phải từ 18 tuổi trở lên.')

    @api.constrains('ngay_vao_lam', 'ngay_nghi_viec')
    def _check_ngay_lam_viec(self):
        for record in self:
            if record.ngay_vao_lam and record.ngay_nghi_viec and record.ngay_nghi_viec < record.ngay_vao_lam:
                raise ValidationError('Ngày nghỉ việc không được nhỏ hơn ngày vào làm.')
