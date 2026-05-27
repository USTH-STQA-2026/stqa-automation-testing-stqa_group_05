"""
Login Tests — Library Book Borrowing System
📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.
"""

import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR

def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)
    COMPLETED — Use as a reference example.
    RIPR:
        [R] Reachability - Navigate Login page
        [I] Infection - Enter valid email and password
        [P] Propagation - Wait for UI to update
        [R] Revealability - Check result
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")

    #Screenshot evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail - wrong password
    RIPR
        [R] Reachability: Go to login page
        [I] Infection: Enter valid email but wrong password
        [P] Propagation: Wait until error appears on UI
        [R] Revealability: Check error message in Flutter semantics tree
    """
    # [R] Reachability: Go to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter valid email but wrong password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["wrongpass"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait until error appears on UI
    wait_for_flutter(page, text="Mật khẩu không đúng")
    
    # Screenshot evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R] Revealability: Check error message in Flutter semantics tree
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text, (
        f"Expect error 'Mật khẩu không đúng' not found. Got {sem_text[:200]}"
    )
        
def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail - empty fields (*Đăng nhập thất bại - để trống các trường*)
    RIPR
        [R] Reachability: Go to login page
        [I] Infection: Click Login immediately
        [P] Propagation: Wait until error appears on UI
        [R] Revealability: Check error message in Flutter semantics tree
    """
    # [R] Reachability: Go to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Click Login immediately
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait until error appears on UI
    wait_for_flutter(page, text="Vui lòng nhập email và mật khẩu")
    
    # Screenshot evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R] Revealability: Check error message in Flutter semantics tree
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập email và mật khẩu" in sem_text, (
       f"Expect error 'Vui lòng nhập email và mật khẩu' not found. Got {sem_text[:200]}"
    )