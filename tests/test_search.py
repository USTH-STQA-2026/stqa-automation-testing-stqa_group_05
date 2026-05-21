"""
Search & Filter Tests — Library Book Borrowing System

TC-04 to TC-07 — COMPLETED.

Key selectors for Flutter Web:
    - Search input : aria-label = "Tìm kiếm theo tên sách hoặc tác giả..."
    - Filter dropdown: aria-label = "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Book card    : flt-semantics[role="group"][aria-label*="Mã: BOOK"]
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
    """TC-04: Search book by name — results found

    COMPLETED
    Flow: Log in → search for "Flutter" → verify BOOK001 appears.

    RIPR:
        [R] Log in, navigate to Books tab
        [I] Enter "Flutter" into the search bar
        [P] System filters the list based on the search query
        [R] Assert books containing "Flutter" are displayed in results
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Input search query
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Smart Wait: wait for the results to load
    wait_for_flutter(page, text="Flutter")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_name_flutter.png"))

    # Assert: at least 1 book containing "Flutter" is displayed
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert results.count() > 0 or "Flutter" in sem_text, (
        "No books found for keyword 'Flutter' — expected at least BOOK001"
    )


def test_search_book_no_result(page, test_config):
    """TC-05: Search book — no results

    COMPLETED
    Flow: Log in → search non-existent keyword → verify 'Không tìm thấy' (Not found) message.

    RIPR:
        [R] Log in, navigate to Books tab
        [I] Enter non-existent keyword "xyz_khong_ton_tai_12345"
        [P] System returns an empty results set
        [R] Assert no book cards are shown or 'Không tìm thấy' message is displayed
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Enter non-existent keyword
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345",
    )

    # Smart Wait: wait for system to process
    wait_for_flutter(page, text="Không tìm thấy")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_no_result.png"))

    # Assert: no book cards shown, or "Không tìm thấy" message is displayed
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_no_books = book_cards.count() == 0
    has_message = "Không tìm thấy" in sem_text
    assert has_no_books or has_message, (
        f"Expected empty result or 'Không tìm thấy' message. "
        f"Book cards found: {book_cards.count()}"
    )


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category

    COMPLETED
    Flow: Log in → filter by "Công nghệ" (Technology) → verify all shown books belong to that category.

    RIPR:
        [R] Log in, navigate to Books tab
        [I] Enter "Công nghệ" into the category filter dropdown
        [P] System filters the list to only display Technology books
        [R] Assert all displayed book cards contain "Công nghệ" in their aria-label
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Enter category to filter
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ",
    )

    # Smart Wait: wait for the list to update
    wait_for_flutter(page, text="Công nghệ")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category_cong_nghe.png"))

    # Assert: all displayed book cards belong to "Công nghệ"
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
    """TC-07: Search book by author name

    COMPLETED
    Flow: Log in → search for "Nguyễn Minh Đức" → verify books by that author are shown.

    RIPR:
        [R] Log in, navigate to Books tab
        [I] Enter author name "Nguyễn Minh Đức" into search input
        [P] System filters books list by author name
        [R] Assert books by "Nguyễn Minh Đức" are in the results
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Search by author name
    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức",
    )

    # Smart Wait: wait for results to load
    wait_for_flutter(page, text="Nguyễn Minh Đức")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert: at least 1 book by "Nguyễn Minh Đức" is displayed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0 or "Nguyễn Minh Đức" in sem_text, (
        "No results found for author 'Nguyễn Minh Đức' — expected BOOK001, BOOK009"
    )


# ---------------------------------------------------------------------------
# BONUS B1 — Extra TC: Case-insensitive search
# REQ-03 requires search to be case-insensitive
# ---------------------------------------------------------------------------

def test_search_case_insensitive(page, test_config):
    """BONUS TC-Extra-02: Case-insensitive search

    REQ-03: Search must be case-insensitive.
    Searching for 'FLUTTER' should yield the same results as searching for 'Flutter'.
    """
    login(page, test_config)

    # Search using uppercase characters
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "FLUTTER")
    wait_for_flutter(page, text="Flutter")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_case_insensitive.png"))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Flutter" in sem_text, (
        "Search 'FLUTTER' (uppercase) should still find 'Flutter' books — REQ-03 case-insensitive"
    )
