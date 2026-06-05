# -*- coding: utf-8 -*-
"""
Member Management Tests — Library Book Borrowing System
REQ-07: Member Management (Add New Member)
Bugs covered: BUG-07, BUG-08, BUG-09, BUG-10, BUG-11
"""

import os

from conftest import (
    SCREENSHOT_DIR,
    enable_flutter_semantics,
    flutter_click_button,
    flutter_fill,
    wait_for_flutter,
)


# A helper to navigate to the Add Member screen as Librarian
def go_to_add_member_screen(page, test_config):
    # Log in as Librarian
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Click "Thêm thành viên" button to open the form
    add_member_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    add_member_btn.click()
    wait_for_flutter(page, text="Thêm thành viên mới")
    enable_flutter_semantics(page)


def test_add_member_valid(page, test_config):
    """TC-25: Add valid member successfully

    Expect: Success message and new member code.
    Actual (BUG-07): System shows "Invalid email" and rejects.
    """
    go_to_add_member_screen(page, test_config)

    flutter_fill(page, "Họ và tên", "Nguyen Test")
    flutter_fill(page, "Email", "testnewuser99@gmail.com")
    flutter_fill(page, "Số điện thoại", "0901234567")

    # Click submit "Thêm thành viên"
    submit_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    submit_btn.click()

    # Wait for success message or validation message
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_valid.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Assert successful addition
    assert "Invalid email" not in sem_text, (
        "Valid email was incorrectly flagged as invalid (BUG-07)"
    )
    assert (
        "thành công" in sem_text or "successfully" in sem_text or "MEM" in sem_text
    ), f"Expected member to be added successfully. Got: {sem_text[:300]}"


def test_add_member_invalid_email(page, test_config):
    """TC-26: Reject invalid email format

    Expect: Show validation/format error, reject addition.
    Actual (BUG-08): System accepts invalid email format "new@gmail" and adds member.
    """
    go_to_add_member_screen(page, test_config)

    flutter_fill(page, "Họ và tên", "Test Invalid Email")
    flutter_fill(page, "Email", "new@gmail")  # missing dot in domain
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_invalid_email.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Assert validation error is shown and member is NOT added
    assert (
        "thành công" not in sem_text
        and "successfully" not in sem_text
        and "MEM00" not in sem_text
    ), "Should not successfully add member with invalid email format (BUG-08)"
    # Check that some form of "invalid email" validation message is shown
    assert "Invalid email" in sem_text or "không hợp lệ" in sem_text, (
        f"Expected invalid email warning message. Got: {sem_text[:300]}"
    )


def test_add_member_duplicate_email(page, test_config):
    """TC-27: Reject duplicate email

    Expect: Reject with error indicating email is already registered/exists.
    Actual (BUG-09): Shows general "Invalid email" instead of duplicate error.
    """
    go_to_add_member_screen(page, test_config)

    flutter_fill(page, "Họ và tên", "Nguyen Duplicate Email")
    flutter_fill(page, "Email", "librarian@library.com")  # existing email
    flutter_fill(page, "Số điện thoại", "0901234567")

    submit_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_duplicate_email.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Assert rejection with correct duplicate message
    assert (
        "thành công" not in sem_text
        and "successfully" not in sem_text
        and "MEM" not in sem_text
    ), "Should not add duplicate email"
    assert (
        "đã tồn tại" in sem_text.lower()
        or "đã đăng ký" in sem_text.lower()
        or "already exists" in sem_text.lower()
        or "duplicate" in sem_text.lower()
    ), f"Expected duplicate email error message. Got: {sem_text[:300]}"


def test_add_member_empty_phone(page, test_config):
    """TC-29: Reject empty phone number

    Expect: Show validation error that phone number is required.
    Actual (BUG-10): Shows "Invalid email" instead of phone validation error.
    """
    go_to_add_member_screen(page, test_config)

    flutter_fill(page, "Họ và tên", "Nguyen Empty Phone")
    flutter_fill(page, "Email", "emptyphone@gmail.com")
    # leave Số điện thoại blank

    submit_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_empty_phone.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "thành công" not in sem_text and "successfully" not in sem_text, (
        "Should not successfully add member with empty phone"
    )
    assert "số điện thoại" in sem_text.lower() or "phone" in sem_text.lower(), (
        f"Expected phone requirement validation error. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "Should not show 'Invalid email' for empty phone (BUG-10)"
    )


def test_add_member_invalid_phone(page, test_config):
    """TC-30: Reject invalid phone number format

    Expect: Show phone format validation error.
    Actual (BUG-11): Shows "Invalid email" instead of phone format error.
    """
    go_to_add_member_screen(page, test_config)

    flutter_fill(page, "Họ và tên", "Nguyen Invalid Phone")
    flutter_fill(page, "Email", "invalidphone@gmail.com")
    flutter_fill(page, "Số điện thoại", "09abcde345")  # letters in phone

    submit_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên")'
    )
    submit_btn.click()

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "add_member_invalid_phone.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "thành công" not in sem_text and "successfully" not in sem_text, (
        "Should not successfully add member with invalid phone format"
    )
    assert "số điện thoại" in sem_text.lower() or "phone" in sem_text.lower(), (
        f"Expected phone format validation error. Got: {sem_text[:300]}"
    )
    assert "Invalid email" not in sem_text, (
        "Should not show 'Invalid email' for invalid phone (BUG-11)"
    )
