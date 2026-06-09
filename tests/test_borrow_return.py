# -*- coding: utf-8 -*-
"""
Borrow & Return Tests — Library Book Borrowing System

This file contains the core test cases TC-08 to TC-10 and Bonus test cases
verifying system bugs discovered in manual testing (BUG-03, BUG-04, BUG-05,
BUG-06, BUG-12).

Textbook concepts in this file:
  - RIPR Model (Ch.2): Reachability, Infection, Propagation, Revealability
  - Oracle Strength (Ch.14): Strong assertions on text content and UI changes
  - Regression Testing (Ch.13): Automating tests to detect verified bugs

Seed data notes:
    - MEM002 (ba.nguyen@email.com) already has BR001 (BOOK003) "Đang mượn" (Borrowed)
    - BOOK001 (Lập trình Flutter cơ bản) — status: Có sẵn (Available) → used for TC-08
    - BOOK003 (Kiểm thử phần mềm nhập môn) — borrowed by MEM002 → used for TC-10
"""
import os
import re
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    login,
    SCREENSHOT_DIR,
)


def click_confirm_borrow_button(page):
    """Helper: Click the confirmation 'Mượn' button inside the modal dialog.

    Uses a regex match to avoid strictness conflicts with 'Mượn sách này' in the book list.
    """
    confirm_btn = page.locator('flt-semantics[role="button"]').filter(has_text=re.compile(r"^Mượn$")).first
    confirm_btn.click()


# ---------------------------------------------------------------------------
# Core Test Cases (TC-08 to TC-10)
# ---------------------------------------------------------------------------

def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book successfully

    Flow: Log in → find an "Available" book → click "Mượn sách này"
          → confirm dialog → check book status changes to "Đang mượn".

    RIPR Model:
        [R] Reachability  → Log in, navigate to Books tab
        [I] Infection     → Click 'Mượn sách này' on an 'Available' book, confirm modal dialog
        [P] Propagation   → System processes transaction, updates book status in memory
        [R] Revealability → Assert success message or verify book status changed to 'Đang mượn'
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Find an Available book and borrow it
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=15000)

    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    # [P] Propagation: Wait for confirmation dialog to appear
    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)

    # Confirm loan (click "Mượn" in modal dialog)
    flutter_click_button(page, "Mượn")

    # Wait for success toast/notification
    wait_for_flutter(page, text="thành công", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # [R] Revealability: Assert success
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đang mượn" in sem_text, (
        "Expected 'thành công' or 'Đang mượn' after borrowing"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list

    Flow: Log in → navigate to 'Mượn / Trả' tab → verify loan records appear.

    RIPR Model:
        [R] Reachability  → Log in, navigate to page (user has active loan BR001 in seed data)
        [I] Infection     → Click the 'Mượn / Trả' tab
        [P] Propagation   → System renders list of active loans
        [R] Revealability → Assert presence of loan records with 'Trả sách' button
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Click the "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()

    # [P] Propagation: Wait for tab content to render
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # [R] Revealability: Assert loan records are present
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrow_records = "Trả sách" in sem_text or "Đang mượn" in sem_text
    assert has_borrow_records, (
        "No borrowed books shown in 'Mượn / Trả' tab — "
        "MEM002 should have BR001 (BOOK003) from seed data"
    )


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book

    Flow: Log in → tab 'Mượn / Trả' → click 'Trả sách' → verify successful return.

    RIPR Model:
        [R] Reachability  → Log in, navigate to 'Mượn / Trả' tab
        [I] Infection     → Click 'Trả sách' button on record BR001
        [P] Propagation   → System processes return transaction, updates book status to 'Có sẵn'
        [R] Revealability → Assert success message or verify status updated to 'Đã trả'
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # Navigate to "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    # [I] Act: Click the "Trả sách" button on the first loan card
    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    return_btn.click()

    # [P] Propagation: Wait for operation result message
    wait_for_flutter(page, text="thành công", timeout=15000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # [R] Revealability: Assert successful return
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đã trả" in sem_text, (
        "Expected success message or 'Đã trả' status after returning book"
    )


# ---------------------------------------------------------------------------
# Bonus Test Cases (B1 - Verification of Manual Bugs)
# ---------------------------------------------------------------------------

def test_borrow_suspended_member(page, test_config):
    """Bonus B1: Suspended member cannot borrow books (BUG-04 / manual TC-15)

    Expect: Reject borrowing and display suspended account warning.
    Actual (BUG-04): System correctly rejects borrow but displays wrong message
           ("Member has expired. Cannot borrow book." instead of Suspended status warning).

    RIPR Model:
        [R] Reachability  → Log in as Suspended member (cu.le@email.com)
        [I] Infection     → Click 'Mượn sách này' on an 'Available' book, click 'Mượn'
        [P] Propagation   → System detects suspended status, shows validation message
        [R] Revealability → Assert warning specifically contains "tạm ngưng" / "suspended"
                           and NOT "hết hạn" / "expired" (BUG-04 validation)
    """
    # [R] Arrange: Log in as suspended member
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "cu.le@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # [I] Act: Click borrow button on first available book
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="attached", timeout=15000)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)
    click_confirm_borrow_button(page)

    # [P] Propagation: Wait for response validation message
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_suspended_member.png"))

    # [R] Revealability: Assert BUG-04 (shows expired message instead of suspended message)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "tạm ngưng" in sem_text.lower() or "suspended" in sem_text.lower(), (
        f"BUG-04: Expected suspended warning. Got: {sem_text[:300]}"
    )
    assert "hết hạn" not in sem_text.lower() and "expired" not in sem_text.lower(), (
        "BUG-04: Should not display expired error message for suspended account"
    )


def test_borrow_limit_exceeded(page, test_config):
    """Bonus B1: Member cannot borrow more than 3 books (BUG-03 / manual TC-17)

    Expect: Reject borrowing the 4th book and show limit exceeded warning.
    Actual (BUG-03): System allows borrowing the 4th book successfully.

    RIPR Model:
        [R] Reachability  → Log in as regular active member (dam.tran@email.com)
        [I] Infection     → Borrow 3 books successfully, then attempt to borrow a 4th book
        [P] Propagation   → System checks borrow count limit constraint
        [R] Revealability → Assert that borrowing the 4th book is rejected (BUG-03 check)
    """
    # [R] Arrange: Log in
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "dam.tran@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # [I] Act: Borrow 3 books successfully first
    for i in range(3):
        available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
        available_book.wait_for(state="attached", timeout=15000)
        borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
        borrow_btn.click()

        wait_for_flutter(page, text="Mượn", timeout=15000)
        enable_flutter_semantics(page)
        click_confirm_borrow_button(page)

        wait_for_flutter(page, text="thành công", timeout=15000)
        enable_flutter_semantics(page)
        page.wait_for_timeout(2000)

    # Attempt to borrow the 4th book
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="attached", timeout=15000)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    wait_for_flutter(page, text="Mượn", timeout=15000)
    enable_flutter_semantics(page)
    click_confirm_borrow_button(page)

    # [P] Propagation: Wait for response
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_limit_exceeded.png"))

    # [R] Revealability: Assert BUG-03 (success message should not be shown)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in sem_text and "successful" not in sem_text, (
        "BUG-03: System allowed borrowing the 4th book, violating the 3-book limit constraint"
    )


def test_return_overdue_warning(page, test_config):
    """Bonus B1: Returning overdue book displays warning (BUG-05 / manual TC-19)

    Expect: Success message and an overdue warning notification.
    Actual (BUG-05): Return successful but no overdue warning is displayed.

    RIPR Model:
        [R] Reachability  → Log in as MEM002 (has overdue BR001 in seed data)
        [I] Infection     → Go to 'Mượn / Trả' tab, click 'Trả sách' on overdue BR001
        [P] Propagation   → System completes return and evaluates overdue status
        [R] Revealability → Assert that an overdue warning is displayed (BUG-05 check)
    """
    # [R] Arrange
    login(page, test_config)

    # [I] Act: Go to tab and click Return on the overdue book (BR001)
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    # [P] Propagation: Wait for success dialog
    wait_for_flutter(page, text="thành công", timeout=15000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_overdue_warning.png"))

    # [R] Revealability: Assert BUG-05 (should show warning text "quá hạn" or "overdue")
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "quá hạn" in sem_text.lower() or "overdue" in sem_text.lower(), (
        "BUG-05: Overdue book returned successfully but no overdue warning was displayed"
    )


def test_return_other_member_book(page, test_config):
    """Bonus B1: Cannot return another member's book (BUG-06 / manual TC-28)

    Expect: Reject return action or hide/disable Return button for other members' slips.
    Actual (BUG-06): Successfully returns another member's book via slip lookup.

    RIPR Model:
        [R] Reachability  → Log in as member MEM002, navigate to 'Mượn / Trả' tab
        [I] Infection     → Look up MEM006's slips and click 'Trả sách' button on BR003
        [P] Propagation   → System evaluates authorization and processes return
        [R] Revealability → Assert that return is rejected (BUG-06 check)
    """
    # [R] Arrange
    login(page, test_config)

    # Navigate to "Mượn / Trả" tab
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    # [I] Act: Look up MEM006's borrowing slips
    sub_tab = page.locator('flt-semantics[role="tab"][aria-label*="Tra cứu phiếu mượn"], flt-semantics:has-text("Tra cứu phiếu mượn")').first
    sub_tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Nhập mã thành viên (VD: MEM001)", "MEM006")
    flutter_click_button(page, "Tra cứu")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Attempt to click "Trả sách" on the retrieved slip
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    if "Trả sách" in sem_text:
        return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
        return_btn.click()
        try:
            wait_for_flutter(page, text="thành công", timeout=5000)
        except Exception:
            page.wait_for_timeout(2000)
        enable_flutter_semantics(page)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_other_member_book.png"))
        sem_text_after = " ".join(page.locator("flt-semantics").all_text_contents())

        # [R] Revealability: Assert BUG-06 (should not allow return)
        assert "thành công" not in sem_text_after, (
            "BUG-06: Allowed returning another member's book (MEM006's slip) via unauthorized return action"
        )


def test_unauthorized_slip_lookup(page, test_config):
    """Bonus B1: Member cannot lookup another member's slip (BUG-12 / manual TC-27)

    Expect: Reject lookup or hide details of another member's slip.
    Actual (BUG-12): Displays other member's record details.

    RIPR Model:
        [R] Reachability  → Log in as MEM002, navigate to 'Mượn / Trả' tab
        [I] Infection     → Input other member ID 'MEM006' and click 'Tra cứu'
        [P] Propagation   → System checks lookup authorization
        [R] Revealability → Assert that lookup is rejected or details are not shown (BUG-12 check)
    """
    # [R] Arrange
    login(page, test_config)

    # [I] Act: Look up other member's ID (MEM006)
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách", timeout=15000)
    enable_flutter_semantics(page)

    sub_tab = page.locator('flt-semantics[role="tab"][aria-label*="Tra cứu phiếu mượn"], flt-semantics:has-text("Tra cứu phiếu mượn")').first
    sub_tab.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Nhập mã thành viên (VD: MEM001)", "MEM006")
    flutter_click_button(page, "Tra cứu")

    # [P] Propagation: Wait to see if MEM006's slip info loads (e.g., name "Hoàng Cá Biệt")
    try:
        wait_for_flutter(page, text="Hoàng Cá Biệt", timeout=8000)
        success = True
    except Exception:
        success = False

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "unauthorized_slip_lookup.png"))

    # [R] Revealability: Assert BUG-12 (lookup should have failed)
    assert not success, (
        "BUG-12: Member successfully looked up another member's borrowing slip details"
    )
