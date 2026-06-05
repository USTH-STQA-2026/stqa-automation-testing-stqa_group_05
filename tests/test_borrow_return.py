# -*- coding: utf-8 -*-
"""
Borrow & Return Tests — Library Book Borrowing System

TC-08 to TC-10 — COMPLETED.

Seed data notes:
    - MEM002 (ba.nguyen@email.com) already has BR001 (BOOK003) "Đang mượn" (Borrowed)
    - BOOK001 (Lập trình Flutter cơ bản) — status: Có sẵn (Available) → used for TC-08
    - BOOK003 (Kiểm thử phần mềm nhập môn) — borrowed by MEM002 → used for TC-10

Note: If tests ran previously in the same session, seed data may be modified.
    To reset: login as librarian → click "Đặt lại dữ liệu" before re-running.

Key selectors:
    - Tab "Mượn / Trả" : flt-semantics[role="tab"][aria-label="Mượn / Trả"]
    - Available Book   : flt-semantics[role="group"][aria-label*="Có sẵn"]
    - Borrow button    : flt-semantics[role="button"]:has-text("Mượn sách này")
    - Return button    : flt-semantics[role="button"]:has-text("Trả sách")
"""

import os
import re

from conftest import (
    SCREENSHOT_DIR,
    enable_flutter_semantics,
    flutter_click_button,
    flutter_fill,
    login,
    wait_for_flutter,
)


def click_confirm_borrow_button(page):
    """Clicks the confirmation 'Mượn' button exactly using a regex match to avoid strictness conflicts with 'Mượn sách này'."""
    confirm_btn = (
        page.locator('flt-semantics[role="button"]')
        .filter(has_text=re.compile(r"^Mượn$"))
        .first
    )
    confirm_btn.click()


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book

    COMPLETED
    Flow: Log in → find an "Available" book → click "Mượn sách này" (Borrow this book)
          → confirm dialog → check book status changes to "Đang mượn" (Borrowed).

    RIPR:
        [R] Log in, navigate to Books tab
        [I] Click 'Mượn sách này' on an 'Available' book, confirm modal dialog
        [P] System processes transaction, updates book status
        [R] Assert success message or verify book status changed to 'Đang mượn'
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Find an Available book and borrow it
    # Wait up to 15s for at least one "Có sẵn" (Available) book card to appear
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=15000)

    # Click the "Mượn sách này" button inside the selected available book card
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    # [P] Propagation: Wait for confirmation dialog to appear
    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)

    # Confirm loan (click "Mượn" in modal dialog strictly)
    click_confirm_borrow_button(page)

    # Wait for success toast/notification
    wait_for_flutter(page, text="thành công", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # [R] Assert: success notification OR book status changed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đang mượn" in sem_text, (
        "Expected 'thành công' or 'Đang mượn' after borrowing — borrow may have failed"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list

    COMPLETED
    Flow: Log in → navigate to 'Mượn / Trả' (Borrow / Return) tab → verify loan records appear.

    Note: MEM002 (default test user) has BR001 (BOOK003) active in seed data,
    so the tab will always display at least one active record right after login.

    RIPR:
        [R] Log in, rely on test database state (MEM002 has active loan record)
        [I] Click the 'Mượn / Trả' tab
        [P] System renders list of active loans
        [R] Assert presence of loan records with 'Trả sách' button or 'Đang mượn' text
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Click the "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()

    # [P] Wait for tab content to render (Smart Wait)
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # [R] Assert: loan records are present (checking for "Trả sách" button or "Đang mượn" status text)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrow_records = "Trả sách" in sem_text or "Đang mượn" in sem_text
    assert has_borrow_records, (
        "No borrowed books shown in 'Mượn / Trả' tab — "
        "MEM002 should have BR001 (BOOK003) from seed data"
    )


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book

    COMPLETED
    Flow: Log in → tab 'Mượn / Trả' → click 'Trả sách' (Return) → verify successful return.

    Note: MEM002 has BR001 (BOOK003) in seed data.
    After return, book reverts to 'Có sẵn' and record updates to 'Đã trả' (Returned).

    RIPR:
        [R] Log in, navigate to 'Mượn / Trả' tab (MEM002 has active loan record)
        [I] Click 'Trả sách' button on record BR001
        [P] System processes return transaction, updates book and record status
        [R] Assert success message or verify status updated to 'Đã trả'
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # Navigate to "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    # [I] Act: Click the "Trả sách" button on the first loan card (MEM002's BR001)
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    # [P] Wait for operation result message
    wait_for_flutter(page, text="thành công", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # [R] Assert: successful return (checking for success notification or "Đã trả" status text)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đã trả" in sem_text, (
        "Expected success message or 'Đã trả' status after returning book"
    )


# ---------------------------------------------------------------------------
# BUG-03: Wrong error message when suspended account borrows a book
# ---------------------------------------------------------------------------


def test_borrow_suspended_member(page, test_config):
    """TC-18: Suspended member receives suspended-account message

    Expect: Reject borrowing with a message indicating account suspension.
    Actual (BUG-03): Rejects but displays expired-account message instead.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "cu.le@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=15000)
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)
    click_confirm_borrow_button(page)

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_suspended_member.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "tạm ngưng" in sem_text.lower() or "suspended" in sem_text.lower(), (
        f"Expected suspended account warning. Got: {sem_text[:300]}"
    )
    assert "hết hạn" not in sem_text.lower() and "expired" not in sem_text.lower(), (
        "Should not display 'expired'/'hết hạn' error message for a suspended account"
    )


# ---------------------------------------------------------------------------
# BUG-04: Member can borrow more than 3 books
# ---------------------------------------------------------------------------


def test_borrow_limit_exceeded(page, test_config):
    """TC-20: Member cannot borrow more than 3 books

    Expect: Reject borrowing the 4th book and show limit exceeded warning.
    Actual (BUG-04): System allows borrowing the 4th book successfully.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "dam.tran@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Borrow 3 books successfully
    for _ in range(3):
        available_book = page.locator(
            'flt-semantics[role="group"][aria-label*="Có sẵn"]'
        ).first
        available_book.wait_for(state="attached", timeout=15000)
        borrow_btn = available_book.locator(
            'flt-semantics[role="button"]:has-text("Mượn sách này")'
        )
        borrow_btn.click()

        wait_for_flutter(page, text="Mượn", timeout=15000)
        enable_flutter_semantics(page)
        click_confirm_borrow_button(page)

        wait_for_flutter(page, text="thành công", timeout=15000)
        enable_flutter_semantics(page)
        page.wait_for_timeout(2000)

    # Try borrowing the 4th book
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=15000)
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)
    click_confirm_borrow_button(page)

    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_limit_exceeded.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "thành công" not in sem_text and "successful" not in sem_text, (
        "Borrowing the 4th book should be rejected per limit constraint"
    )


# ---------------------------------------------------------------------------
# BUG-05: No overdue warning displayed when returning an overdue book
# ---------------------------------------------------------------------------


def test_return_overdue_warning(page, test_config):
    """TC-22: Returning overdue book displays warning

    Expect: Success message and an overdue warning.
    Actual (BUG-05): Return successful but no overdue warning is displayed.
    """
    login(page, test_config)

    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    wait_for_flutter(page, text="thành công", timeout=15000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_overdue_warning.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "quá hạn" in sem_text.lower() or "overdue" in sem_text.lower(), (
        "Should display an overdue warning when returning an overdue book"
    )


# ---------------------------------------------------------------------------
# BUG-06: Member can return another member's book
# ---------------------------------------------------------------------------


def test_return_other_member_book(page, test_config):
    """TC-23: Cannot return another member's book

    Expect: Reject return action or disable/hide Return button for other member's slip.
    Actual (BUG-06): Successfully returns other member's book.
    """
    login(page, test_config)

    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    sub_tab = page.locator(
        'flt-semantics[role="tab"][aria-label*="Tra cứu phiếu mượn"], flt-semantics:has-text("Tra cứu phiếu mượn")'
    ).first
    sub_tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Nhập mã thành viên (VD: MEM001)", "MEM006")
    flutter_click_button(page, "Tra cứu")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    if "Trả sách" in sem_text:
        return_btn = page.locator(
            'flt-semantics[role="button"]:has-text("Trả sách")'
        ).first
        return_btn.click()
        wait_for_flutter(page, text="thành công", timeout=5000)
        enable_flutter_semantics(page)
        sem_text_after = " ".join(page.locator("flt-semantics").all_text_contents())

        assert "thành công" not in sem_text_after, (
            "Should not allow returning another member's book"
        )


# ---------------------------------------------------------------------------
# BUG-12: Member can look up another member's borrowing slip
# ---------------------------------------------------------------------------


def test_unauthorized_slip_lookup(page, test_config):
    """TC-33: Member cannot lookup another member's slip

    Expect: Reject look up or do not display other member's record details.
    Actual (BUG-12): Displays other member's record details.
    """
    login(page, test_config)

    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    sub_tab = page.locator(
        'flt-semantics[role="tab"][aria-label*="Tra cứu phiếu mượn"], flt-semantics:has-text("Tra cứu phiếu mượn")'
    ).first
    sub_tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Nhập mã thành viên (VD: MEM001)", "MEM006")
    flutter_click_button(page, "Tra cứu")

    # Wait for search results to load and verify if they contain unauthorized info.
    # If the bug exists, we will successfully load MEM006's details ('Hoàng Cá Biệt' or 'BR003').
    try:
        wait_for_flutter(page, text="Hoàng Cá Biệt", timeout=8000)
        success = True
    except Exception:
        success = False

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "unauthorized_slip_lookup.png"))
    assert not success, (
        "Security violation: Member successfully looked up another member's borrowing slip (BUG-12)"
    )
