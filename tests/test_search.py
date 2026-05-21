"""
Search & Filter Tests — Kiểm thử Tìm kiếm & Lọc sách — Library Book Borrowing System

TC-04 đến TC-07 — ĐÃ HOÀN THÀNH.

Key selectors cho Flutter Web:
    - Ô tìm kiếm  : aria-label = "Tìm kiếm theo tên sách hoặc tác giả..."
    - Ô lọc       : aria-label = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Card sách   : flt-semantics[role="group"][aria-label*="Mã: BOOK"]
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


def test_search_book_by_name(page, test_config):
    """TC-04: Tìm kiếm sách theo tên — có kết quả (Search book by name — results found)

    ✅ COMPLETED
    Flow: Đăng nhập → tìm "Flutter" → kiểm tra BOOK001 xuất hiện.

    📖 RIPR:
        [R] Đăng nhập, vào tab Sách
        [I] Nhập "Flutter" vào ô tìm kiếm
        [P] Hệ thống lọc danh sách theo từ khóa
        [R✓] Assert có sách chứa "Flutter" trong kết quả
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập từ khóa tìm kiếm
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Smart Wait: chờ kết quả hiển thị
    wait_for_flutter(page, text="Flutter")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_name_flutter.png"))

    # Assert: có ít nhất 1 sách chứa "Flutter" trong kết quả
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert results.count() > 0 or "Flutter" in sem_text, (
        "No books found for keyword 'Flutter' — expected at least BOOK001"
    )


def test_search_book_no_result(page, test_config):
    """TC-05: Tìm kiếm sách — không có kết quả (Search book — no results)

    ✅ COMPLETED
    Flow: Đăng nhập → tìm từ khóa không tồn tại → kiểm tra thông báo 'Không tìm thấy'.

    📖 RIPR:
        [R] Đăng nhập, vào tab Sách
        [I] Nhập từ khóa "xyz_khong_ton_tai_12345" không có trong DB
        [P] Hệ thống trả về kết quả rỗng
        [R✓] Assert không có thẻ sách nào hiển thị hoặc có thông báo 'Không tìm thấy'
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập từ khóa không tồn tại
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345",
    )

    # Smart Wait: chờ hệ thống xử lý
    wait_for_flutter(page, text="Không tìm thấy")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_no_result.png"))

    # Assert: không có thẻ sách nào, hoặc có thông báo "Không tìm thấy"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_no_books = book_cards.count() == 0
    has_message = "Không tìm thấy" in sem_text
    assert has_no_books or has_message, (
        f"Expected empty result or 'Không tìm thấy' message. "
        f"Book cards found: {book_cards.count()}"
    )


def test_filter_by_category(page, test_config):
    """TC-06: Lọc sách theo thể loại 'Công nghệ' (Filter books by category)

    ✅ COMPLETED
    Flow: Đăng nhập → lọc "Công nghệ" → tất cả sách hiển thị phải thuộc thể loại đó.

    📖 RIPR:
        [R] Đăng nhập, vào tab Sách
        [I] Nhập "Công nghệ" vào ô lọc thể loại
        [P] Hệ thống lọc chỉ hiển thị sách Công nghệ
        [R✓] Assert tất cả thẻ sách hiển thị đều chứa "Công nghệ" trong aria-label
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập thể loại cần lọc
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ",
    )

    # Smart Wait: chờ danh sách cập nhật
    wait_for_flutter(page, text="Công nghệ")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category_cong_nghe.png"))

    # Assert: tất cả thẻ sách hiển thị đều thuộc "Công nghệ"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()
    assert count > 0, "No books found after filtering by 'Công nghệ'"

    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, (
            f"Book at index {i} does NOT belong to 'Công nghệ'. "
            f"aria-label: '{label}'"
        )


def test_search_by_author(page, test_config):
    """TC-07: Tìm kiếm sách theo tên tác giả (Search book by author name)

    ✅ COMPLETED
    Flow: Đăng nhập → tìm "Nguyễn Minh Đức" → kiểm tra có sách của tác giả đó.

    📖 RIPR:
        [R] Đăng nhập, vào tab Sách
        [I] Nhập tên tác giả "Nguyễn Minh Đức" vào ô tìm kiếm
        [P] Hệ thống lọc danh sách theo tên tác giả
        [R✓] Assert có sách của tác giả "Nguyễn Minh Đức" trong kết quả
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Tìm kiếm theo tên tác giả
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức",
    )

    # Smart Wait: chờ kết quả hiển thị
    wait_for_flutter(page, text="Nguyễn Minh Đức")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert: có ít nhất 1 sách của tác giả "Nguyễn Minh Đức"
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0 or "Nguyễn Minh Đức" in sem_text, (
        "No results found for author 'Nguyễn Minh Đức' — expected BOOK001, BOOK009"
    )


# ---------------------------------------------------------------------------
# 🎁 BONUS B1 — Extra TC: Tìm kiếm không phân biệt HOA/thường
# REQ-03 yêu cầu tìm kiếm case-insensitive
# ---------------------------------------------------------------------------

def test_search_case_insensitive(page, test_config):
    """BONUS TC-Extra-02: Tìm kiếm không phân biệt HOA/thường (Case-insensitive search)

    REQ-03: Tìm kiếm KHÔNG phân biệt chữ hoa/thường (case-insensitive).
    Kết quả tìm 'FLUTTER' phải giống kết quả tìm 'Flutter'.
    """
    login(page, test_config)

    # Tìm bằng chữ HOA
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "FLUTTER")
    wait_for_flutter(page, text="Flutter")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_case_insensitive.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Flutter" in sem_text, (
        "Search 'FLUTTER' (uppercase) should still find 'Flutter' books — REQ-03 case-insensitive"
    )
