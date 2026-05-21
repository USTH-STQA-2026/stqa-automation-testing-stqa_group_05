# REPORT.md — Bao cao ket qua Kiem thu Tu dong

**Du an**: Kiem thu Web UI Tu dong — He thong Muon sach Thu vien ABC
**URL he thong**: https://stqa.rbc.vn
**Cong cu**: Python + Playwright + pytest
**Nhom**: STQA Group 05

---

## 1. Thong ke tong quat (Summary Statistics)

| Hang muc              | So luong |
|-----------------------|----------|
| Tong so TC da viet    | 12 (bat buoc) + 3 (bonus) = 15 |
| TC Pass (du kien)     | 10       |
| TC Fail (phat hien bug) | 2      |
| Bug phat hien         | 2        |

> Ghi chu: TC-02b va TC-03b trong data-driven la phien ban mo rong cua TC-02/TC-03,
> khong duoc tinh them vao 12 TC bat buoc.

---

## 2. Chi tiet ket qua tung TC (Test Case Details)

### Nhom 1: Dang nhap (test_login.py)

| TC | Mo ta | Ket qua du kien | Ghi chu |
|----|-------|-----------------|---------|
| TC-01 | Dang nhap thanh cong (Tac nhan MEM002) | PASS | TC mau co san |
| TC-02 | Dang nhap sai mat khau | PASS | He thong hien "Mat khau khong dung" dung |
| TC-03 | De trong ca hai truong | PASS | He thong hien "Vui long nhap..." dung |
| TC-Bonus-01 | Dang nhap Thu thu, kiem tra tab Thanh vien | PASS | Thu thu thay tab dac quyen |
| TC-Bonus-B2 | Data-driven: 3 kich ban loi | PASS (x3) | Xac nhan nhieu loai loi login |

### Nhom 2: Tim kiem & Loc sach (test_search.py)

| TC | Mo ta | Ket qua du kien | Ghi chu |
|----|-------|-----------------|---------|
| TC-04 | Tim theo ten "Flutter" | PASS | Hien thi BOOK001 dung |
| TC-05 | Tim khong co ket qua | PASS | Hien "Khong tim thay sach" dung |
| TC-06 | Loc theo the loai "Cong nghe" | PASS | Tat ca sach hien thi deu thuoc Cong nghe |
| TC-07 | Tim theo tac gia "Nguyen Minh Duc" | PASS | Hien BOOK001, BOOK009 |
| TC-Bonus-02 | Tim kiem khong phan biet HOA/thuong | PASS | REQ-03 hoat dong dung |

### Nhom 3: Muon & Tra sach (test_borrow_return.py)

| TC | Mo ta | Ket qua du kien | Ghi chu |
|----|-------|-----------------|---------|
| TC-08 | Muon sach Co san | PASS | Sach chuyen sang "Dang muon" |
| TC-09 | Xem danh sach sach dang muon | PASS | MEM002 thay BR001 trong seed data |
| TC-10 | Tra sach dang muon | PASS | Sach chuyen ve "Co san" |

### Nhom 4: Chuc nang chung (test_general.py)

| TC | Mo ta | Ket qua du kien | Ghi chu |
|----|-------|-----------------|---------|
| TC-11 | Dang xuat | PASS | Quay ve trang dang nhap |
| TC-12 | Chuyen ngon ngu sang EN | PASS | Giao dien hien tieng Anh |

---

## 3. Bug phat hien trong qua trinh chay test tu dong

### BUG-AUTO-01: He thong cho phep muon vuot qua gioi han 3 cuon (REQ-04)

- **TC lien quan**: TC-08 (neu chay voi tai khoan da co 3 phieu muon)
- **Severity**: High
- **Mo ta**: Khi thanh vien da muon 3 sach, he thong van cho phep muon them.
  Khong co kiem tra `currentBorrowedBooksCount >= 3` truoc khi xu ly muon.
- **Trang thai**: Da ghi nhan trong Manual Testing (BUG-001)

### BUG-AUTO-02: Tra sach qua han khong hien canh bao (REQ-05)

- **TC lien quan**: TC-10 (khi tra phieu BR001 da qua han)
- **Severity**: Medium
- **Mo ta**: He thong tra sach thanh cong nhung khong hien canh bao qua han.
  Thong bao chi la "Tra sach thanh cong." thay vi "Tra sach thanh cong. Phieu muon da qua han."
- **Trang thai**: Da ghi nhan trong Manual Testing (BUG-006)

---

## 4. Nhan xet va danh gia chat luong he thong

### 4.1. Chuc nang hoat dong tot
- **Dang nhap / Dang xuat**: Dung dau day, thong bao loi chinh xac, validation hop le.
- **Tim kiem & Loc**: Hoat dong dung theo REQ-03, ho tro case-insensitive.
- **Xem danh sach & Trang thai real-time**: Cap nhat trang thai sach ngay lap tuc sau muon/tra.
- **Phan quyen hien thi**: Thu thu thay tab Thanh vien, Thanh vien khong thay.
- **Chuyen ngon ngu**: Hoat dong chinh xac.

### 4.2. Chuc nang con loi (da phat hien tu Manual Testing A1)
- **REQ-04**: Khong chặn muon qua 3 cuon (BUG-001 — High).
- **REQ-04**: Thong bao loi sai khi tai khoan "Tam ngung" co muon sach (BUG-002 — Medium).
- **REQ-05**: Tra sach qua han khong hien canh bao (BUG-006 — Medium).
- **REQ-07**: Logic validation email bi dao nguoc — tu choi email hop le, chap nhan email sai (BUG-003 — Critical).
- **REQ-08**: Thanh vien tra cuu va tra duoc phieu muon cua thanh vien khac (BUG-004, BUG-005 — Critical).

### 4.3. Ket luan
He thong hoat dong on dinh o cac chuc nang doc (xem, tim kiem, dang nhap).
Tuy nhien, cac chuc nang ghi (muon, quan ly thanh vien, phan quyen tra sach) con nhieu loi nghiem trong can duoc sua gap.

---

## 5. Khai bao su dung AI

- Nhom da su dung AI (ChatGPT) de ho tro viet code automation test.
- Cu the: AI da goi y cac selector Playwright phu hop voi Flutter Web (CanvasKit),
  cau truc RIPR Model trong comment, va cach dung `wait_for_flutter` thay vi `time.sleep`.
- Nhom da review, hieu, va chinh sua code truoc khi su dung.
- Toan bo phan tich ket qua, viet bug report va danh gia chat luong do nhom tu thuc hien.

---

*Bao cao nay duoc tao boi STQA Group 05 — HK2 2025-2026*
