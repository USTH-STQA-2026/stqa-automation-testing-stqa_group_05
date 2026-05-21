"""
Login Tests — Kiểm thử Đăng nhập — Library Book Borrowing System

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See Bonus B2

This file contains 1 completed example (TC-01).
TC-02 and TC-03 completed by student.
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    SCREENSHOT_DIR,
)


def test_login_success(page, test_config):
    """TC-01: Đăng nhập thành công với thông tin hợp lệ (Login success with valid credentials)

    ✅ COMPLETED — Use as a reference example.

    📖 RIPR Model (Textbook Ch.2):
        [R] Reachability  → Truy cập trang đăng nhập
        [I] Infection     → Nhập dữ liệu hợp lệ
        [P] Propagation   → Chờ UI cập nhật
        [R✓] Revealability → Kiểm tra kết quả
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI (Smart Wait)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, (
        f"Login failed: '{test_config['display_name']}' or Logout button not found"
    )


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Đăng nhập thất bại — sai mật khẩu (Login fail — wrong password)

    ✅ COMPLETED
    📖 RIPR:
        [R] Truy cập trang đăng nhập
        [I] Nhập email đúng, mật khẩu SAI
        [P] Hệ thống xử lý → lỗi lan truyền ra thông báo "Mật khẩu không đúng"
        [R✓] Assert thông báo lỗi xuất hiện, KHÔNG có nút Đăng xuất
    """
    # [R] Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Nhập email đúng, mật khẩu SAI
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "sai_mat_khau_invalid_999")
    flutter_click_button(page, "Đăng nhập")

    # [P] Chờ thông báo lỗi xuất hiện (Smart Wait)
    wait_for_flutter(page, text="Mật khẩu không đúng")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R✓] Kiểm tra: có thông báo lỗi, KHÔNG đăng nhập thành công
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text, (
        f"Expected error 'Mật khẩu không đúng' not found. Got: {sem_text[:200]}"
    )
    assert "Đăng xuất" not in sem_text, (
        "User should NOT be logged in after wrong password"
    )


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Đăng nhập thất bại — để trống các trường (Login fail — empty fields)

    ✅ COMPLETED
    📖 RIPR:
        [R] Truy cập trang đăng nhập
        [I] KHÔNG nhập gì, click Đăng nhập → kích hoạt validation
        [P] Hệ thống từ chối → thông báo "Vui lòng nhập email và mật khẩu"
        [R✓] Assert thông báo lỗi xuất hiện, vẫn ở trang đăng nhập
    """
    # [R] Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] KHÔNG nhập gì — click Đăng nhập ngay
    flutter_click_button(page, "Đăng nhập")

    # [P] Chờ thông báo lỗi (Smart Wait)
    wait_for_flutter(page, text="Vui lòng nhập")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R✓] Kiểm tra: thông báo lỗi hiện ra, không đăng nhập được
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập" in sem_text, (
        f"Expected validation error not found. Got: {sem_text[:200]}"
    )
    assert "Đăng xuất" not in sem_text, (
        "User should NOT be logged in when fields are empty"
    )


# ---------------------------------------------------------------------------
# 🎁 BONUS B2 — Data-Driven Testing (@pytest.mark.parametrize)
# Gộp nhiều kịch bản đăng nhập thất bại vào 1 hàm test
# Textbook Ch.3 §3.3.2: Data-driven testing tăng coverage với ít code hơn
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("email, password, expected_error, tc_id", [
    # Sai mật khẩu
    ("ba.nguyen@email.com", "sai_mat_khau_invalid", "Mật khẩu không đúng", "TC-02b"),
    # Bỏ trống cả hai
    ("", "", "Vui lòng nhập", "TC-03b"),
    # Email không tồn tại trong hệ thống
    ("nobody@test.com", "password123", "Không tìm thấy", "TC-Login-Extra"),
])
def test_login_fail_parametrized(page, test_config, email, password, expected_error, tc_id):
    """BONUS B2 — Data-Driven: nhiều kịch bản đăng nhập thất bại

    Kiểm thử hướng dữ liệu: cùng một flow test nhưng với các bộ dữ liệu khác nhau.
    (Data-driven testing: same test flow with different input datasets.)
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # Chờ thông báo lỗi
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"login_fail_{tc_id}.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, (
        f"[{tc_id}] Expected '{expected_error}' not found. Got: {sem_text[:300]}"
    )
    assert "Đăng xuất" not in sem_text, f"[{tc_id}] Should not be logged in"


# ---------------------------------------------------------------------------
# 🎁 BONUS B1 — Extra TC: Đăng nhập Thủ thư
# Kiểm tra vai trò Thủ thư có đặc quyền (thấy tab Thành viên — REQ-07)
# ---------------------------------------------------------------------------

def test_login_as_librarian(page, test_config):
    """BONUS TC-Extra-01: Đăng nhập với vai trò Thủ thư (Login as Librarian)

    Kiểm tra tài khoản Thủ thư đăng nhập thành công và thấy tab Thành viên
    (chức năng chỉ Thủ thư mới có — REQ-07).
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_librarian.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    # Thủ thư phải thấy tab "Thành viên" — Thành viên bình thường không thấy
    assert "Thành viên" in sem_text, (
        "Librarian should see the 'Thành viên' tab (REQ-07)"
    )
    assert "Đăng xuất" in sem_text, "Librarian login should succeed"
