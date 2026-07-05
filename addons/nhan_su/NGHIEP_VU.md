# Phân tích nghiệp vụ module Quản lý nhân sự

## 1. Quản lý hồ sơ nhân viên

Module lưu trữ thông tin định danh và thông tin liên hệ của nhân viên: mã nhân viên, họ tên, ngày sinh, giới tính, CCCD/CMND, email, số điện thoại, địa chỉ, ảnh và trạng thái làm việc.

Nghiệp vụ chính:
- Tạo và cập nhật hồ sơ nhân viên.
- Kiểm tra mã nhân viên và số CCCD/CMND không trùng.
- Tự tính tuổi từ ngày sinh.
- Chặn hồ sơ nhân viên dưới 18 tuổi.
- Theo dõi trạng thái: hồ sơ mới, đang làm việc, tạm nghỉ, đã nghỉ việc.

## 2. Quản lý cơ cấu tổ chức

Đơn vị đại diện cho phòng ban/bộ phận trong doanh nghiệp. Mỗi đơn vị có mã, tên, đơn vị cấp trên và mô tả.

Nghiệp vụ chính:
- Khai báo danh mục đơn vị.
- Tổ chức đơn vị theo cấp cha - con.
- Thống kê số nhân viên hiện tại của từng đơn vị dựa trên lịch sử công tác đang hiệu lực.

## 3. Quản lý chức vụ

Chức vụ là danh mục vị trí công tác như nhân viên, trưởng phòng, giám đốc.

Nghiệp vụ chính:
- Khai báo mã và tên chức vụ.
- Sử dụng chức vụ trong quá trình công tác của nhân viên.
- Kiểm tra mã chức vụ không trùng.

## 4. Quản lý lịch sử công tác

Lịch sử công tác ghi nhận nhân viên làm việc tại đơn vị nào, giữ chức vụ gì, trong khoảng thời gian nào.

Nghiệp vụ chính:
- Gắn nhân viên với đơn vị và chức vụ.
- Phân biệt chức vụ chính và chức vụ kiêm nhiệm.
- Theo dõi ngày bắt đầu, ngày kết thúc và trạng thái đang hiệu lực.
- Tự xác định đơn vị/chức vụ hiện tại trên hồ sơ nhân viên từ lịch sử công tác chính còn hiệu lực.
- Chặn ngày kết thúc nhỏ hơn ngày bắt đầu.

## 5. Quản lý chứng chỉ/bằng cấp

Danh mục chứng chỉ/bằng cấp mô tả loại bằng cấp, chứng chỉ, kỹ năng hoặc loại khác. Danh sách chứng chỉ của nhân viên ghi nhận văn bằng cụ thể nhân viên đang có.

Nghiệp vụ chính:
- Khai báo danh mục chứng chỉ/bằng cấp.
- Gắn chứng chỉ/bằng cấp vào từng nhân viên.
- Lưu số hiệu, nơi cấp, ngày cấp, ngày hết hạn và tệp đính kèm.
- Tự xác định chứng chỉ còn hiệu lực, hết hiệu lực hoặc chưa xác định thời hạn.
- Chặn ngày hết hạn nhỏ hơn ngày cấp.
