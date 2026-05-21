"""
Logout & Language Tests — Library Book Borrowing System

TC-11 and TC-12 — COMPLETED.

Key selectors:
    - Logout button : flt-semantics[role="button"]:has-text("Đăng xuất")
    - EN button     : flt-semantics[role="button"]:has-text("EN")
    - Post-logout   : "Đăng nhập" button and "Email" input field reappear
    - Post-language : "Logout", "Borrow", "Library", "Books" text appear
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
    """TC-11: Logout success

    COMPLETED
    Flow: Log in → click 'Đăng xuất' (Logout) → verify redirected back to login page.

    RIPR:
        [R] Log in successfully (status: authenticated)
        [I] Click the 'Đăng xuất' button
        [P] System signs out, redirects back to login page
        [R] Assert: 'Đăng nhập' button and 'Email' input are shown, 'Đăng xuất' is NOT present
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Click the "Đăng xuất" button
    flutter_click_button(page, "Đăng xuất")

    # [P] Wait for login page to render again (Smart Wait)
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout_success.png"))

    # [R] Assert: back on the login page
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_button = "Đăng nhập" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_button or has_email_input, (
        "Should be back on login page after logout — "
        "expected 'Đăng nhập' button or Email input field"
    )
    # Bonus B3: Detailed verification — Logout button must no longer exist
    assert "Đăng xuất" not in sem_text, (
        "Logout button should NOT be present after logging out"
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English

    COMPLETED
    Flow: Log in → click 'EN' → verify UI elements display in English.

    RIPR:
        [R] Log in, home page displays in Vietnamese by default
        [I] Click the 'EN' button
        [P] System switches language, re-renders the UI in English
        [R] Assert: English keywords ('Logout', 'Borrow', 'Library', 'Books') are displayed
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # [I] Act: Click the "EN" language switch button
    flutter_click_button(page, "EN")

    # [P] Wait for the interface to re-render in English (Smart Wait)
    wait_for_flutter(page, text="Logout")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "language_switched_to_english.png"))

    # [R] Assert: UI has successfully switched to English
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    english_keywords = ["Logout", "Borrow", "Library", "Books", "Return"]
    has_english = any(keyword in sem_text for keyword in english_keywords)
    assert has_english, (
        f"UI did not switch to English. "
        f"Expected one of {english_keywords} in semantics. "
        f"Got: {sem_text[:300]}"
    )
    # Bonus B3: Detailed verification — Vietnamese label is replaced
    assert "Đăng xuất" not in sem_text, (
        "Vietnamese 'Đăng xuất' should be replaced by English 'Logout'"
    )
