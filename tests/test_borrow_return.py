"""
Borrow & Return Tests — Kiểm thử Mượn & Trả sách — Library Book Borrowing System

TC-08 đến TC-10 — ĐÃ HOÀN THÀNH.

Ghi chú seed data (dữ liệu reset mỗi lần mở trang mới / fresh context):
    - MEM002 (ba.nguyen@email.com) đã có BR001 (BOOK003) "Đang mượn" trong seed data
    - BOOK001 (Lập trình Flutter cơ bản) — trạng thái: Có sẵn → dùng cho TC-08
    - BOOK003 (Kiểm thử phần mềm nhập môn) — Đã mượn bởi MEM002 → dùng cho TC-10

Key selectors:
    - Tab "Mượn / Trả" : flt-semantics[role="tab"][aria-label="Mượn / Trả"]
    - Sách Có sẵn      : flt-semantics[role="group"][aria-label*="Có sẵn"]
    - Nút mượn         : flt-semantics[role="button"]:has-text("Mượn sách này")
    - Nút trả          : flt-semantics[role="button"]:has-text("Trả sách")
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
    """TC-08: Mượn sách có trạng thái 'Có sẵn' (Borrow an available book)

    ✅ COMPLETED
    Flow: Đăng nhập → tìm sách 'Có sẵn' → click 'Mượn sách này' → xác nhận dialog
          → kiểm tra sách chuyển sang 'Đang mượn'.

    📖 RIPR:
        [R] Đăng nhập, ở tab Sách
        [I] Click 'Mượn sách này' trên sách 'Có sẵn', xác nhận dialog
        [P] Hệ thống xử lý mượn sách, cập nhật trạng thái
        [R✓] Assert thông báo 'thành công' hoặc sách chuyển sang 'Đang mượn'
    """
    # [R] Arrange: Đăng nhập
    login(page, test_config)

    # [I] Act: Tìm sách Có sẵn và mượn
    available_book = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    ).first
    available_book.wait_for(state="attached", timeout=10000)

    # Click nút "Mượn sách này" bên trong thẻ sách Có sẵn đó
    borrow_btn = available_book.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    )
    borrow_btn.click()

    # [P] Propagation: Chờ dialog xác nhận hiện ra
    wait_for_flutter(page, text="Mượn")
    enable_flutter_semantics(page)

    # Xác nhận mượn sách (click nút "Mượn" trong dialog)
    flutter_click_button(page, "Mượn")

    # Chờ thông báo thành công
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "borrow_book_success.png"))

    # [R✓] Assert: thông báo thành công HOẶC sách đã đổi trạng thái
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đang mượn" in sem_text, (
        "Expected 'thành công' or 'Đang mượn' after borrowing — borrow may have failed"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: Xem danh sách sách đang mượn (View borrowed books list)

    ✅ COMPLETED
    Flow: Đăng nhập → chuyển sang tab 'Mượn / Trả' → kiểm tra có hiển thị phiếu mượn.

    Ghi chú: MEM002 (tài khoản test mặc định) đã có BR001 (BOOK003) trong seed data,
    nên tab 'Mượn / Trả' sẽ luôn có ít nhất 1 phiếu mượn ngay sau khi đăng nhập.

    📖 RIPR:
        [R] Đăng nhập, mọi phụ thuộc dữ liệu (MEM002 đã có phiếu mượn sẵn)
        [I] Click tab 'Mượn / Trả'
        [P] Hệ thống hiển thị danh sách phiếu mượn
        [R✓] Assert có phiếu mượn, có nút 'Trả sách' hoặc text 'Đang mượn'
    """
    # [R] Arrange: Đăng nhập (MEM002 đã có BR001 trong seed data)
    login(page, test_config)

    # [I] Act: Chuyển sang tab "Mượn / Trả"
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()

    # [P] Chờ nội dung tab load xong
    wait_for_flutter(page, text="Trả sách")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "view_borrowed_books.png"))

    # [R✓] Assert: có phiếu mượn (có nút "Trả sách" hoặc text "Đang mượn")
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrow_records = "Trả sách" in sem_text or "Đang mượn" in sem_text
    assert has_borrow_records, (
        "No borrowed books shown in 'Mượn / Trả' tab — "
        "MEM002 should have BR001 (BOOK003) from seed data"
    )


def test_return_book(page, test_config):
    """TC-10: Trả sách đang mượn (Return a borrowed book)

    ✅ COMPLETED
    Flow: Đăng nhập → tab 'Mượn / Trả' → click 'Trả sách' → kiểm tra trả thành công.

    Ghi chú: MEM002 có BR001 (BOOK003) trong seed data.
    Sau khi trả, sách chuyển về 'Có sẵn', phiếu đổi sang 'Đã trả'.

    📖 RIPR:
        [R] Đăng nhập, vào tab 'Mượn / Trả' (MEM002 có phiếu BR001 sẵn có)
        [I] Click 'Trả sách' trên phiếu BR001
        [P] Hệ thống xử lý trả sách, cập nhật trạng thái sách và phiếu
        [R✓] Assert thông báo 'thành công' hoặc trạng thái 'Đã trả'
    """
    # [R] Arrange: Đăng nhập
    login(page, test_config)

    # Chuyển sang tab "Mượn / Trả"
    tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    tab.click()
    wait_for_flutter(page, text="Trả sách")
    enable_flutter_semantics(page)

    # [I] Act: Click nút "Trả sách" (phiếu đầu tiên — BR001 của MEM002)
    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    return_btn.click()

    # [P] Chờ thông báo kết quả
    wait_for_flutter(page, text="thành công")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "return_book_success.png"))

    # [R✓] Assert: trả thành công (thông báo "thành công" hoặc phiếu đổi sang "Đã trả")
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in sem_text or "Đã trả" in sem_text, (
        "Expected success message or 'Đã trả' status after returning book"
    )
