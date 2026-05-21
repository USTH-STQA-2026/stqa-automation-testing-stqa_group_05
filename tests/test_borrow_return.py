"""
Borrow & Return Tests — Library Book Borrowing System

TC-08 to TC-10 — COMPLETED.

Seed data notes (resets on fresh context creation):
    - MEM002 (ba.nguyen@email.com) already has BR001 (BOOK003) "Đang mượn" (Borrowed) in seed data
    - BOOK001 (Lập trình Flutter cơ bản) — status: Có sẵn (Available) → used for TC-08
    - BOOK003 (Kiểm thử phần mềm nhập môn) — borrowed by MEM002 → used for TC-10

Key selectors:
    - Tab "Mượn / Trả" : flt-semantics[role="tab"][aria-label="Mượn / Trả"]
    - Available Book   : flt-semantics[role="group"][aria-label*="Có sẵn"]
    - Borrow button    : flt-semantics[role="button"]:has-text("Mượn sách này")
    - Return button    : flt-semantics[role="button"]:has-text("Trả sách")
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    login,
    SCREENSHOT_DIR,
)


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
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=10000)

    # Click the "Mượn sách này" button inside the selected available book card
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    # [P] Propagation: Wait for confirmation dialog to appear
    wait_for_flutter(page, text="Mượn")
    enable_flutter_semantics(page)

    # Confirm loan (click "Mượn" in modal dialog)
    flutter_click_button(page, "Mượn")

    # Wait for success toast/notification
    wait_for_flutter(page, text="thành công")
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

    # [P] Wait for tab content to render
    wait_for_flutter(page, text="Trả sách")
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
    wait_for_flutter(page, text="Trả sách")
    enable_flutter_semantics(page)

    # [I] Act: Click the "Trả sách" button on the first loan card (MEM002's BR001)
    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    return_btn.click()

    # [P] Wait for operation result message
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # [R] Assert: successful return (checking for success notification or "Đã trả" status text)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đã trả" in sem_text, (
        "Expected success message or 'Đã trả' status after returning book"
    )
