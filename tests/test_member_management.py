# -*- coding: utf-8 -*-
"""
Member Management Tests — Library Book Borrowing System
BONUS B1: Additional test cases beyond TC-01~TC-12 required by ASSIGNMENT.md

These tests cover REQ-07 (Librarian: Add Member) and bug detection corresponding
to the group's manual testing report (TC-30 to TC-36).

Textbook concepts in this file:
  - RIPR Model (Ch.2): [R], [I], [P], [R] steps in each test
  - Oracle Strength (Ch.14): Strong assertions checking specific error messages
  - Regression Testing (Ch.13): Tests that detect system bugs confirmed in manual testing

Bugs detected by this file:
  BUG-07: Valid email rejected as "Invalid email"
  BUG-08: Invalid email format accepted
  BUG-09: Duplicate email shows wrong error
  BUG-10: Empty phone shows wrong error
  BUG-11: Invalid phone format shows wrong error
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


def go_to_add_member_screen(page, test_config):
    """Helper: Log in as Librarian and navigate to the Add Member form."""
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất", timeout=15000)
    enable_flutter_semantics(page)

    add_member_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    add_member_btn.click()
    wait_for_flutter(page, text="Thêm thành viên mới", timeout=10000)
    enable_flutter_semantics(page)


def test_bonus_b1_view_member_list(page, test_config):
    """BONUS B1 — TC-30: Librarian can view detailed member information

    Each member's info must include: name, member ID, email, phone, status.
    Verifies Active (MEM002), Suspended (MEM004), and Expired (MEM005) statuses.

    RIPR:
        [R] Log in as Librarian, navigate to Thành viên (Members) tab
        [I] Members tab renders the member list
        [P] System displays all member records with their details
        [R] Assert name, ID, email, phone, and all 3 status types are present
    """
    # [R] Arrange: Log in as Librarian
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất", timeout=15000)
    enable_flutter_semantics(page)

    # [I] Act: Click the "Thành viên" (Members) tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Thành viên"]')
    tab.click()
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_view_member_list.png"))

    # [R] Assert: Member details visible — Bonus B3 (strong assertions on specific text)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Nguyễn Học Bá" in sem_text, "Missing member name: Nguyễn Học Bá"
    assert "MEM002" in sem_text, "Missing member ID: MEM002"
    assert "ba.nguyen@email.com" in sem_text, "Missing member email"
    assert "0901234567" in sem_text, "Missing member phone"
    assert "Hoạt động" in sem_text, "Missing Active (Hoạt động) status"
    assert "Lê Cần Cù" in sem_text, "Missing suspended member: Lê Cần Cù"
    assert "Tạm ngưng" in sem_text, "Missing Suspended (Tạm ngưng) status"
    assert "Phạm Trung Bình" in sem_text, "Missing expired member: Phạm Trung Bình"
    assert "Hết hạn" in sem_text, "Missing Expired (Hết hạn) status"


def test_bonus_b1_add_member_valid(page, test_config):
    """BONUS B1 — TC-31: Librarian adds a member with valid data

    Expected (SRS): New member is added, code generated and displayed.
    Actual (BUG-07): System rejects valid email with 'Email không hợp lệ'.

    This test FAILS because the system has BUG-07.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit valid name, email, phone
        [P] System processes creation request
        [R] Assert success — new MEM code shown (BUG-07: actually shows 'Invalid email')
    """
    # [R] Arrange: Open Add Member form
    go_to_add_member_screen(page, test_config)

    # [I] Act: Fill in valid member data
    flutter_fill(page, "Họ và tên", "Nguyen Test")
    flutter_fill(page, "Email", "testnewuser99@gmail.com")
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Wait for response
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_valid.png"))

    # [R] Assert: BUG-07 — valid email should NOT be rejected
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Invalid email" not in sem_text, (
        "BUG-07: Valid email 'testnewuser99@gmail.com' was incorrectly flagged as invalid"
    )
    assert "thành công" in sem_text or "successfully" in sem_text or "MEM" in sem_text, (
        f"Expected member to be added successfully. Got: {sem_text[:300]}"
    )


def test_bonus_b1_add_member_invalid_email(page, test_config):
    """BONUS B1 — TC-32: System rejects invalid email format

    Expected (SRS): Reject 'new@gmail' (missing domain extension) with error.
    Actual (BUG-08): System accepts invalid email format and adds member.

    This test FAILS because the system has BUG-08.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit invalid email 'new@gmail' (missing .com/.net/etc.)
        [P] System validates email
        [R] Assert rejection — BUG-08: actually accepts and creates member
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Fill in invalid email format
    flutter_fill(page, "Họ và tên", "Test Invalid")
    flutter_fill(page, "Email", "new@gmail")  # missing dot in domain
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_invalid_email.png"))

    # [R] Assert: BUG-08 — invalid email should be rejected
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "MEM00" not in sem_text, (
        "BUG-08: Invalid email format 'new@gmail' was accepted — should be rejected"
    )
    assert "Invalid email" in sem_text or "không hợp lệ" in sem_text, (
        f"Expected invalid email warning. Got: {sem_text[:300]}"
    )


def test_bonus_b1_add_member_duplicate_email(page, test_config):
    """BONUS B1 — TC-33: System rejects duplicate email

    Expected (SRS): Reject duplicate email with specific 'email already exists' error.
    Actual (BUG-09): Shows generic 'Email không hợp lệ' instead of duplicate error.

    This test FAILS because the system has BUG-09.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit existing email 'librarian@library.com'
        [P] System detects duplicate
        [R] Assert specific duplicate error — BUG-09: shows generic invalid email error
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Use existing email
    flutter_fill(page, "Họ và tên", "Nguyen Duplicate")
    flutter_fill(page, "Email", "librarian@library.com")  # existing email
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_duplicate_email.png"))

    # [R] Assert: BUG-09 — should show duplicate error, not generic email error
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "MEM" not in sem_text, (
        "Should not add member with duplicate email"
    )
    assert ("đã tồn tại" in sem_text.lower() or "đã đăng ký" in sem_text.lower()
            or "already exists" in sem_text.lower() or "duplicate" in sem_text.lower()), (
        f"BUG-09: Expected duplicate email error, got generic message: {sem_text[:300]}"
    )


def test_bonus_b1_add_member_empty_name(page, test_config):
    """BONUS B1 — TC-34: System rejects empty full name

    Expected: Reject with 'Full name must not be blank' validation error.
    This test PASSES — the system correctly validates empty name.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit form with empty name field
        [P] System validates name requirement
        [R] Assert name validation error is displayed
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Leave name blank
    flutter_fill(page, "Email", "valid@email.com")
    flutter_fill(page, "Số điện thoại", "0901234567")
    # Họ và tên intentionally left empty

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_empty_name.png"))

    # [R] Assert: Name validation error shown — Bonus B3 (strong oracle)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "successfully" not in sem_text, (
        "Should not add member with empty name"
    )
    assert ("họ và tên" in sem_text.lower() or "tên" in sem_text.lower()
            or "name" in sem_text.lower() or "blank" in sem_text.lower()
            or "không được để trống" in sem_text.lower()), (
        f"Expected name validation warning. Got: {sem_text[:300]}"
    )


def test_bonus_b1_add_member_empty_phone(page, test_config):
    """BONUS B1 — TC-35: System rejects empty phone number

    Expected (SRS): Reject with 'Phone number must not be blank'.
    Actual (BUG-10): Shows 'Email không hợp lệ' instead of phone validation error.

    This test FAILS because the system has BUG-10.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit form with empty phone field
        [P] System validates phone requirement
        [R] Assert phone error — BUG-10: shows wrong 'Invalid email' message
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Leave phone blank
    flutter_fill(page, "Họ và tên", "Nguyen Phone")
    flutter_fill(page, "Email", "valid2@email.com")
    # Số điện thoại intentionally left empty

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_empty_phone.png"))

    # [R] Assert: BUG-10 — should show phone error, not 'Invalid email'
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text, "Should not add member with empty phone"
    assert "số điện thoại" in sem_text.lower() or "phone" in sem_text.lower(), (
        f"Expected phone validation error. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "BUG-10: Should not show 'Invalid email' for empty phone number"
    )


def test_bonus_b1_add_member_invalid_phone(page, test_config):
    """BONUS B1 — TC-36: System rejects invalid phone number format

    Expected (SRS): Reject with 'Invalid phone number format'.
    Actual (BUG-11): Shows 'Email không hợp lệ' instead of phone format error.

    This test FAILS because the system has BUG-11.

    RIPR:
        [R] Log in as Librarian, open Add Member form
        [I] Submit phone '09abcde345' (contains letters)
        [P] System validates phone format
        [R] Assert phone format error — BUG-11: shows wrong 'Invalid email' message
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Enter invalid phone format (letters in phone number)
    flutter_fill(page, "Họ và tên", "Nguyen Character")
    flutter_fill(page, "Email", "valid3@email.com")
    flutter_fill(page, "Số điện thoại", "09abcde345")  # letters in phone

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "bonus_b1_add_member_invalid_phone.png"))

    # [R] Assert: BUG-11 — should show phone format error, not 'Invalid email'
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text, "Should not add member with invalid phone format"
    assert ("số điện thoại" in sem_text.lower() or "phone" in sem_text.lower()
            or "SĐT" in sem_text or "sđt" in sem_text.lower()), (
        f"BUG-11: Expected phone format error. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "BUG-11: Should not show 'Invalid email' for invalid phone format"
    )
