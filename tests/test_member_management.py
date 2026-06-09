# -*- coding: utf-8 -*-
"""
Member Management Tests — Library Book Borrowing System

This file contains Bonus test cases verifying system bugs discovered in manual
testing for the Librarian's Add Member feature (BUG-07, BUG-08, BUG-09,
BUG-10, BUG-11).

Textbook concepts in this file:
  - RIPR Model (Ch.2): Reachability, Infection, Propagation, Revealability
  - Oracle Strength (Ch.14): Strong assertions on error validation messages
  - Regression Testing (Ch.13): Automating tests to detect verified bugs
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


# ---------------------------------------------------------------------------
# Bonus Test Cases (B1 - Verification of Manual Bugs)
# ---------------------------------------------------------------------------

def test_add_member_valid(page, test_config):
    """Bonus B1: Add member successfully with valid details (BUG-07 / manual TC-21)

    Expect (SRS): Member is successfully added, member code is shown.
    Actual (BUG-07): System incorrectly rejects valid email with "Invalid email" error message.

    RIPR Model:
        [R] Reachability  → Log in as Librarian, open Add Member form
        [I] Infection     → Input valid name, valid email (testnewuser99@gmail.com), valid phone
        [P] Propagation   → Click "Thêm thành viên", system validates inputs
        [R] Revealability → Assert member is added and code shown (BUG-07 checks for invalid rejection)
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Fill valid details
    flutter_fill(page, "Họ và tên", "Nguyen Test")
    flutter_fill(page, "Email", "testnewuser99@gmail.com")
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Propagation: Wait for response validation
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_valid.png"))

    # [R] Revealability: Assert BUG-07 (valid email should not be rejected)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Invalid email" not in sem_text, (
        "BUG-07: Valid email 'testnewuser99@gmail.com' was incorrectly rejected as 'Invalid email'"
    )
    assert "thành công" in sem_text or "successfully" in sem_text or "MEM" in sem_text, (
        f"Expected member to be created successfully. Got: {sem_text[:300]}"
    )


def test_add_member_invalid_email(page, test_config):
    """Bonus B1: System rejects invalid email format (BUG-08 / manual TC-22)

    Expect (SRS): System rejects email with missing dot extension (e.g. 'new@gmail').
    Actual (BUG-08): System incorrectly accepts 'new@gmail' and adds member.

    RIPR Model:
        [R] Reachability  → Log in as Librarian, open Add Member form
        [I] Infection     → Input invalid email 'new@gmail' (missing domain extension)
        [P] Propagation   → Click "Thêm thành viên", system validates email regex
        [R] Revealability → Assert that registration is rejected (BUG-08 check)
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Fill invalid email
    flutter_fill(page, "Họ và tên", "Test Invalid")
    flutter_fill(page, "Email", "new@gmail")  # invalid domain part per SRS
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Propagation: Wait for response validation
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_invalid_email.png"))

    # [R] Revealability: Assert BUG-08 (invalid format should not succeed)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "MEM" not in sem_text, (
        "BUG-08: System successfully created a member with invalid email 'new@gmail'"
    )
    assert "Invalid email" in sem_text or "không hợp lệ" in sem_text, (
        f"Expected invalid email error message. Got: {sem_text[:300]}"
    )


def test_add_member_duplicate_email(page, test_config):
    """Bonus B1: System rejects duplicate email (BUG-09 / manual TC-23)

    Expect (SRS): System rejects duplicate email and shows "Email already exists" warning.
    Actual (BUG-09): Shows general "Invalid email" instead of duplicate warning.

    RIPR Model:
        [R] Reachability  → Log in as Librarian, open Add Member form
        [I] Infection     → Input duplicate email 'librarian@library.com' (already exists in system)
        [P] Propagation   → Click "Thêm thành viên", system checks for email uniqueness
        [R] Revealability → Assert that system rejects and shows specific duplicate error (BUG-09 check)
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Use duplicate email
    flutter_fill(page, "Họ và tên", "Nguyen Duplicate")
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Propagation: Wait for response validation
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_duplicate_email.png"))

    # [R] Revealability: Assert BUG-09 (should show duplicate error, not invalid format error)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "MEM" not in sem_text, (
        "System should not allow duplicate email creation"
    )
    assert ("đã tồn tại" in sem_text.lower() or "đã đăng ký" in sem_text.lower()
            or "exists" in sem_text.lower() or "duplicate" in sem_text.lower()), (
        f"BUG-09: Expected specific duplicate email warning. Got generic/incorrect: {sem_text[:300]}"
    )


def test_add_member_empty_phone(page, test_config):
    """Bonus B1: System rejects empty phone number (BUG-10 / manual TC-29/77)

    Expect (SRS): Reject empty phone with validation error "Phone number must not be blank".
    Actual (BUG-10): Shows generic "Invalid email" error message instead.

    RIPR Model:
        [R] Reachability  → Log in as Librarian, open Add Member form
        [I] Infection     → Input valid name and email, leave phone number blank
        [P] Propagation   → Click "Thêm thành viên", system validates fields
        [R] Revealability → Assert phone number error is displayed (BUG-10 check)
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Leave phone empty
    flutter_fill(page, "Họ và tên", "Nguyen Phone")
    flutter_fill(page, "Email", "valid2@email.com")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Propagation: Wait for validation
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_empty_phone.png"))

    # [R] Revealability: Assert BUG-10 (should show phone error, not invalid email error)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text, "Should not add member with empty phone"
    assert "số điện thoại" in sem_text.lower() or "phone" in sem_text.lower(), (
        f"Expected phone validation warning. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "BUG-10: Should not show 'Invalid email' for empty phone number"
    )


def test_add_member_invalid_phone(page, test_config):
    """Bonus B1: System rejects invalid phone format (BUG-11 / manual TC-30/75/76)

    Expect (SRS): Reject invalid phone with validation error "Invalid phone number format".
    Actual (BUG-11): Shows generic "Invalid email" error message instead.

    RIPR Model:
        [R] Reachability  → Log in as Librarian, open Add Member form
        [I] Infection     → Input invalid phone '09abcde345' (contains characters)
        [P] Propagation   → Click "Thêm thành viên", system validates phone format
        [R] Revealability → Assert phone format error is displayed (BUG-11 check)
    """
    # [R] Arrange
    go_to_add_member_screen(page, test_config)

    # [I] Act: Fill invalid phone
    flutter_fill(page, "Họ và tên", "Nguyen Character")
    flutter_fill(page, "Email", "valid3@email.com")
    flutter_fill(page, "Số điện thoại", "09abcde345")

    submit_btn = page.locator('flt-semantics[role="button"]:has-text("Thêm thành viên")')
    submit_btn.click()

    # [P] Propagation: Wait for validation
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_invalid_phone.png"))

    # [R] Revealability: Assert BUG-11 (should show phone format error, not invalid email error)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text, "Should not add member with invalid phone format"
    assert ("số điện thoại" in sem_text.lower() or "phone" in sem_text.lower()
            or "SĐT" in sem_text or "sđt" in sem_text.lower()), (
        f"BUG-11: Expected phone format validation error. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "BUG-11: Should not show 'Invalid email' for invalid phone format"
    )
