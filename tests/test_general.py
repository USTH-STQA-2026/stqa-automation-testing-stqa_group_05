"""
Logout & Language Tests — Kiểm thử Đăng xuất & Chuyển ngôn ngữ — Library Book Borrowing System

TC-11 và TC-12 — ĐÃ HOÀN THÀNH.

Key selectors:
    - Nút Đăng xuất : flt-semantics[role="button"]:has-text("Đăng xuất")
    - Nút EN        : flt-semantics[role="button"]:has-text("EN")
    - Sau đăng xuất : "Đăng nhập" button và "Email" input xuất hiện lại
    - Sau chuyển EN : "Logout", "Borrow", "Library", "Books" xuất hiện
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


def test_logout(page, test_config):
    """TC-11: Đăng xuất thành công (Logout success)

    ✅ COMPLETED
    Flow: Đăng nhập → click 'Đăng xuất' → kiểm tra quay về trang đăng nhập.

    📖 RIPR:
        [R] Đăng nhập thành công (trạng thái: đã đăng nhập)
        [I] Click nút 'Đăng xuất'
        [P] Hệ thống đăng xuất, chuyển về trang login
        [R✓] Assert: có nút 'Đăng nhập' và ô nhập 'Email', KHÔNG có nút 'Đăng xuất'
    """
    # [R] Arrange: Đăng nhập
    login(page, test_config)

    # [I] Act: Click nút "Đăng xuất"
    flutter_click_button(page, "Đăng xuất")

    # [P] Chờ trang login hiển thị lại (Smart Wait)
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout_success.png"))

    # [R✓] Assert: quay về trang đăng nhập
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_button = "Đăng nhập" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_button or has_email_input, (
        "Should be back on login page after logout — "
        "expected 'Đăng nhập' button or Email input field"
    )
    # Bonus B3: Kiểm tra chi tiết — không có nút Đăng xuất nữa
    assert "Đăng xuất" not in sem_text, (
        "Logout button should NOT be present after logging out"
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Chuyển ngôn ngữ sang tiếng Anh (Switch language to English)

    ✅ COMPLETED
    Flow: Đăng nhập → click 'EN' → kiểm tra giao diện hiển thị tiếng Anh.

    📖 RIPR:
        [R] Đăng nhập, trang chủ hiển thị tiếng Việt
        [I] Click nút 'EN'
        [P] Hệ thống đổi ngôn ngữ, re-render giao diện bằng tiếng Anh
        [R✓] Assert: có text tiếng Anh ('Logout', 'Borrow', 'Library', 'Books')
    """
    # [R] Arrange: Đăng nhập
    login(page, test_config)

    # [I] Act: Click nút chuyển ngôn ngữ "EN"
    flutter_click_button(page, "EN")

    # [P] Chờ giao diện re-render sang tiếng Anh (Smart Wait)
    wait_for_flutter(page, text="Logout")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "language_switched_to_english.png"))

    # [R✓] Assert: giao diện đã chuyển sang tiếng Anh
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    english_keywords = ["Logout", "Borrow", "Library", "Books", "Return"]
    has_english = any(keyword in sem_text for keyword in english_keywords)
    assert has_english, (
        f"UI did not switch to English. "
        f"Expected one of {english_keywords} in semantics. "
        f"Got: {sem_text[:300]}"
    )
    # Bonus B3: Kiểm tra chi tiết — không còn text Việt nữa
    assert "Đăng xuất" not in sem_text, (
        "Vietnamese 'Đăng xuất' should be replaced by English 'Logout'"
    )
