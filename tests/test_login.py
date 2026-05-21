"""
Login Tests — Library Book Borrowing System

Textbook concepts in this file:
  - RIPR Model (Ch.2): See [R], [I], [P], [R] comments in TC-01
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
    """TC-01: Successful login with valid credentials

    COMPLETED — Use as a reference example.

     RIPR Model (Textbook Ch.2):
        [R] Reachability  → Navigate to the login page
        [I] Infection     → Input valid credentials
        [P] Propagation   → Wait for the UI to update
        [R] Revealability → Verify the test result
    """
    # [R] Reachability: Navigate to login page — reach target UI
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter valid credentials — trigger login logic
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for state to propagate to UI (Smart Wait)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R] Revealability: Verify test result — Test Oracle
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, (
        f"Login failed: '{test_config['display_name']}' or Logout button not found"
    )


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Failed login — wrong password

    COMPLETED
    RIPR:
        [R] Navigate to the login page
        [I] Enter valid email, but WRONG password
        [P] System processes → error message "Mật khẩu không đúng" propagates to UI
        [R] Assert error message is visible, and Logout button is NOT present
    """
    # [R] Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Enter valid email, WRONG password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "sai_mat_khau_invalid_999")
    flutter_click_button(page, "Đăng nhập")

    # [P] Wait for the error message to appear (Smart Wait)
    wait_for_flutter(page, text="Mật khẩu không đúng")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R] Verify: error message is displayed, and login did NOT succeed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text, (
        f"Expected error 'Mật khẩu không đúng' not found. Got: {sem_text[:200]}"
    )
    assert "Đăng xuất" not in sem_text, (
        "User should NOT be logged in after wrong password"
    )


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Failed login — empty fields

    COMPLETED
    RIPR:
        [R] Navigate to the login page
        [I] Enter nothing, click Login → triggers validation
        [P] System rejects → validation error "Vui lòng nhập email và mật khẩu"
        [R] Assert error message appears, user remains on login page
    """
    # [R] Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Enter nothing — click Login immediately
    flutter_click_button(page, "Đăng nhập")

    # [P] Wait for validation message (Smart Wait)
    wait_for_flutter(page, text="Vui lòng nhập")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R] Verify: validation message is shown, user is not logged in
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập" in sem_text, (
        f"Expected validation error not found. Got: {sem_text[:200]}"
    )
    assert "Đăng xuất" not in sem_text, (
        "User should NOT be logged in when fields are empty"
    )


# ---------------------------------------------------------------------------
# BONUS B2 — Data-Driven Testing (@pytest.mark.parametrize)
# Combine multiple failed login scenarios into a single test function
# Textbook Ch.3 §3.3.2: Data-driven testing increases coverage with less code
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("email, password, expected_error, tc_id", [
    # Incorrect password
    ("ba.nguyen@email.com", "sai_mat_khau_invalid", "Mật khẩu không đúng", "TC-02b"),
    # Both fields empty
    ("", "", "Vui lòng nhập", "TC-03b"),
    # Email does not exist in system
    ("nobody@test.com", "password123", "Không tìm thấy", "TC-Login-Extra"),
])
def test_login_fail_parametrized(page, test_config, email, password, expected_error, tc_id):
    """BONUS B2 — Data-Driven: multiple failed login scenarios

    Data-driven testing: execute the same test flow with different input datasets.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # Wait for expected error message
    wait_for_flutter(page, text=expected_error)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"login_fail_{tc_id}.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, (
        f"[{tc_id}] Expected '{expected_error}' not found. Got: {sem_text[:300]}"
    )
    assert "Đăng xuất" not in sem_text, f"[{tc_id}] Should not be logged in"


# ---------------------------------------------------------------------------
# BONUS B1 — Extra TC: Librarian login
# Verify librarian role privilege (sees the 'Thành viên' member management tab — REQ-07)
# ---------------------------------------------------------------------------

def test_login_as_librarian(page, test_config):
    """BONUS TC-Extra-01: Login as Librarian

    Verify that a Librarian account can successfully log in and see Librarian-exclusive
    action buttons: "Thêm thành viên" and "Đặt lại dữ liệu" (privileges for Librarians — REQ-07).

    Note: The UI does NOT show a standalone "Thành viên" tab label — instead it shows
    action buttons "Thêm thành viên" (Add member) and "Đặt lại dữ liệu" (Reset data)
    that are exclusive to the Librarian role.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_librarian.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    # Librarian must see exclusive action buttons — REQ-07 privilege check
    # UI shows "Thêm thành viên" (Add member) and "Đặt lại dữ liệu" (Reset data)
    # These buttons are NOT available to regular members (Thành viên role)
    assert "Thêm thành viên" in sem_text or "Đặt lại dữ liệu" in sem_text, (
        "Librarian should see privileged action buttons "
        "('Thêm thành viên' or 'Đặt lại dữ liệu') — REQ-07"
    )
    assert "Đăng xuất" in sem_text, "Librarian login should succeed"
