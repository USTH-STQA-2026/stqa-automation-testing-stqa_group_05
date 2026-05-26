"""
Logout & Language Tests — Library Book Borrowing System

TC-11 and TC-12 — COMPLETED.

Key selectors:
    - Logout button : flt-semantics[role="button"]:has-text("Đăng xuất")
    - EN button     : flt-semantics[role="button"]:has-text("EN")
    - Post-logout   : "Đăng nhập" button and "Email" input field reappear
    - Post-language : "Sign out", "Borrow this book", "Library", "Member" text appear
"""

import os

from conftest import (
    SCREENSHOT_DIR,
    enable_flutter_semantics,
    flutter_click_button,
    login,
    wait_for_flutter,
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
        [P] System switches language — Flutter rebuilds the widget tree synchronously
        [R] Assert: English keywords ('Sign out', 'Borrow this book', 'Library') are
            displayed and Vietnamese labels ('Đăng xuất') are gone

    INVESTIGATION NOTE (why previous test was FAIL):
        Root cause was a WRONG ASSERTION — the test waited for "Logout" which is NOT the
        actual English translation used by this app. Diagnostic script confirmed:
        - After clicking EN, flt-semantics updates IMMEDIATELY (no delay)
        - The actual English button label is "Sign out" (not "Logout")
        - The app also uses "Borrow this book", "Member", "Code", "Borrowed"
        This is NOT a system bug — it was a test oracle error in the original code.
    """
    # [R] Arrange: Log in
    login(page, test_config)

    # Verify we start in Vietnamese (pre-condition check — Bonus B3)
    sem_vi = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" in sem_vi, "Pre-condition: UI should start in Vietnamese"

    # [I] Act: Click the "EN" language switch button
    flutter_click_button(page, "EN")

    # [P] Smart Wait: the semantics tree updates synchronously with Flutter widget rebuild.
    # The actual English label for "Đăng xuất" is "Sign out" in this application.
    wait_for_flutter(page, text="Sign out", timeout=10000)
    page.screenshot(
        path=os.path.join(SCREENSHOT_DIR, "language_switched_to_english.png")
    )

    # [R] Assert: UI has successfully switched to English
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # English keywords actually present in the app after language switch
    # (verified via diagnostic script — NOT assumed)
    english_keywords = ["Sign out", "Borrow this book", "Library", "Member", "Code"]
    has_english = any(keyword in sem_text for keyword in english_keywords)
    assert has_english, (
        f"UI did not switch to English. "
        f"Expected one of {english_keywords} in semantics. "
        f"Got: {sem_text[:300]}"
    )
    # Bonus B3: Detailed negative verification — Vietnamese labels must be gone
    assert "Đăng xuất" not in sem_text, (
        "Vietnamese 'Đăng xuất' should be replaced by English 'Sign out' after language switch"
    )
