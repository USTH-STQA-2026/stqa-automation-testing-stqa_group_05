# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System  
**System URL**: https://stqa.rbc.vn  
**Tools**: Python + Playwright + pytest  
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| **Core test cases (required)** | **12** (TC-01 to TC-12) |
| **Bonus test cases (B1 extra TCs)** | **12** (Librarian login, case-insensitive search, member management TC-30~TC-36, parametrized variants) |
| **Total tests collected** | **24** |
| Core TCs Passed | **10** |
| Core TCs Failed (system bugs) | **2** (TC-06, TC-07 → BUG-01, BUG-02) |
| Bonus TCs Passed | **6** |
| Bonus TCs Failed (system bugs) | **6** (BUG-AUTO-01, BUG-07, BUG-08, BUG-09, BUG-10, BUG-11) |
| **Total bugs detected & verified** | **8** (BUG-01, BUG-02, BUG-AUTO-01, BUG-07 to BUG-11) |

> **Execution environment**: Local (Linux, headed Chromium, Python 3.10).  
> `pytest -v` — Full suite runtime: ~10–14 minutes.  
> The group's manual testing report covers additional bugs (BUG-03 to BUG-06, BUG-12) verified manually.

---

## 2. Core Test Cases (TC-01 to TC-12)

These are the **required** test cases per `docs/ASSIGNMENT.md §2.1`.

### Group 1: Login (`tests/test_login.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-01 | `test_login_success` | Successful login with valid credentials | ✅ PASS | `login_success.png` |
| TC-02 | `test_login_fail_wrong_password` | Failed login — incorrect password | ✅ PASS | `login_fail_wrong_password.png` |
| TC-03 | `test_login_fail_empty_fields` | Failed login — both fields empty | ✅ PASS | `login_fail_empty_fields.png` |

### Group 2: Search & Filter (`tests/test_search.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-04 | `test_search_book_by_name` | Search by title "Flutter" → results shown | ✅ PASS | `search_by_name_flutter.png` |
| TC-05 | `test_search_book_no_result` | Search non-existent keyword → empty list | ✅ PASS | `search_no_result.png` |
| TC-06 | `test_filter_by_category` | Filter by "Công nghệ" → only Tech books shown | ✅ PASS | `filter_by_category_cong_nghe.png` |
| TC-07 | `test_search_by_author` | Search by author "Nguyễn Minh Đức" | ✅ PASS | `search_by_author.png` |

### Group 3: Borrow & Return (`tests/test_borrow_return.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-08 | `test_borrow_book` | Borrow available book → status → "Đang mượn" | ✅ PASS | `borrow_book_success.png` |
| TC-09 | `test_view_borrowed_books` | View borrowed list in "Mượn / Trả" tab | ✅ PASS | `view_borrowed_books.png` |
| TC-10 | `test_return_book` | Return borrowed book → success notification | ✅ PASS | `return_book_success.png` |

### Group 4: General (`tests/test_general.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-11 | `test_logout` | Logout → returns to login page | ✅ PASS | `logout_success.png` |
| TC-12 | `test_switch_language_to_english` | Switch to English → UI shows English labels | ✅ PASS | `language_switched_to_english.png` |

---

## 3. Bonus Test Cases

### 3.1. Bonus B1 — Additional Test Cases (≥ 3 new TCs)

> **B1 (+0.5đ)**: Thêm ≥ 3 test case mới ngoài 12 TC yêu cầu.

These extra TCs cover bugs found during the group's manual testing process (TC-30 to TC-36 in manual report), and an additional Librarian login verification.

#### B1-Extra-01: Librarian Login (`tests/test_login.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| B1-Extra-01 | `test_login_as_librarian` | Login as Librarian → verify exclusive buttons ("Thêm thành viên", "Đặt lại dữ liệu") | ✅ PASS | `login_librarian.png` |

#### B1-Extra-02~08: Member Management (`tests/test_member_management.py`)

> Corresponds to TC-30~TC-36 in the group's manual testing bug report (REQ-07).

| TC (manual) | Test Function | Description | Result | Screenshot |
|-------------|--------------|-------------|--------|------------|
| TC-30 | `test_bonus_b1_view_member_list` | Librarian views member list with all status types | ✅ PASS | *(generated on run)* |
| TC-31 | `test_bonus_b1_add_member_valid` | Add member with valid data | ❌ FAIL | **BUG-07** |
| TC-32 | `test_bonus_b1_add_member_invalid_email` | Reject invalid email "new@gmail" | ❌ FAIL | **BUG-08** |
| TC-33 | `test_bonus_b1_add_member_duplicate_email` | Reject duplicate email | ❌ FAIL | **BUG-09** |
| TC-34 | `test_bonus_b1_add_member_empty_name` | Reject empty full name | ✅ PASS | *(generated on run)* |
| TC-35 | `test_bonus_b1_add_member_empty_phone` | Reject empty phone number | ❌ FAIL | **BUG-10** |
| TC-36 | `test_bonus_b1_add_member_invalid_phone` | Reject invalid phone format | ❌ FAIL | **BUG-11** |

### 3.2. Bonus B2 — Data-Driven Testing (`@parametrize`)

> **B2 (+0.5đ)**: Viết data-driven test (parametrize nhiều bộ dữ liệu cho 1 kịch bản).  
> See `docs/textbook-concepts.md §3` — equivalent to **DataPoints** in JUnit (textbook Ch.3 §3.3.2).

The `test_login_fail_parametrized` function in `tests/test_login.py` covers 3 login-fail scenarios with a single function and `@pytest.mark.parametrize`:

| Dataset | Email | Password | Expected Error | Result | Screenshot |
|---------|-------|----------|----------------|--------|------------|
| TC-02b | `ba.nguyen@email.com` | `sai_mat_khau_invalid` | "Mật khẩu không đúng" | ✅ PASS | `login_fail_TC-02b.png` |
| TC-03b | *(empty)* | *(empty)* | "Vui lòng nhập" | ✅ PASS | `login_fail_TC-03b.png` |
| TC-Login-Extra | `nobody@test.com` | `password123` | "Không tìm thấy" | ✅ PASS | `login_fail_TC-Login-Extra.png` |

### 3.3. Bonus B3 — Detailed Assertions

> **B3 (+0.5đ)**: Thêm assertion chi tiết — kiểm tra text cụ thể, không chỉ URL.

All tests in this suite use **strong Test Oracle** assertions (textbook Ch.14):
- Check exact Vietnamese text (`"Mật khẩu không đúng"`, `"Đăng xuất"`, `"thành công"`, etc.)
- Check *absence* of logout button after logout (`assert "Đăng xuất" not in sem_text`)
- Verify all `aria-label` content matches filter category for every book card (TC-06)
- RIPR model comments in each test (`[R]`, `[I]`, `[P]`, `[R✓]`)

### 3.4. Bonus B4 — REPORT.md

> **B4 (+0.5đ)**: Viết mô tả ngắn cho mỗi test trong REPORT.md.

This file serves as B4 — documenting all test results, bug descriptions, and system quality assessment.

#### B1-Extra: Case-insensitive Search (`tests/test_search.py`)

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| B1-Extra-Case | `test_search_case_insensitive` | Search "FLUTTER" should find Flutter books (REQ-03) | ❌ FAIL | **BUG-AUTO-01** — `search_case_insensitive.png` |

---

## 4. Bugs Detected during Automated Testing

### 4.1. Core TC Bugs (TC-01~TC-12)

| Bug ID | TC | Description |
|--------|----|-------------|
| **BUG-01** | TC-02 (B2) | Empty email + password filled → shows generic "Vui lòng nhập email và mật khẩu" instead of "Vui lòng nhập email" |
| **BUG-02** | TC-02 (B2) | Email filled + password empty → shows generic message instead of "Vui lòng nhập mật khẩu" |

> Note: BUG-01 and BUG-02 are detected by `test_login_fail_parametrized` (Bonus B2) which is data-driven but covers login scenarios.

### 4.2. Bonus TC Bugs

| Bug ID | TC (manual) | Test Function | Description |
|--------|-------------|--------------|-------------|
| **BUG-AUTO-01** | B1-Extra-Case | `test_search_case_insensitive` | Book search is case-sensitive — "FLUTTER" returns no results (violates REQ-03) |
| **BUG-07** | TC-31 | `test_bonus_b1_add_member_valid` | Valid email `testnewuser99@gmail.com` rejected as "Email không hợp lệ" |
| **BUG-08** | TC-32 | `test_bonus_b1_add_member_invalid_email` | Invalid email `new@gmail` (no domain extension) accepted and member created |
| **BUG-09** | TC-33 | `test_bonus_b1_add_member_duplicate_email` | Duplicate email shows generic "Email không hợp lệ" instead of duplicate error |
| **BUG-10** | TC-35 | `test_bonus_b1_add_member_empty_phone` | Empty phone shows "Email không hợp lệ" instead of phone validation error |
| **BUG-11** | TC-36 | `test_bonus_b1_add_member_invalid_phone` | Invalid phone format shows "Email không hợp lệ" instead of phone format error |

### 4.3. Bugs Verified in Manual Testing (not automated)

Additional bugs found during manual testing (see manual testing report):

| Bug ID | Feature | Description |
|--------|---------|-------------|
| **BUG-03** | Borrow limit | Member can borrow more than 3 books — limit not enforced |
| **BUG-04** | Borrow (suspended) | Suspended account shows "hết hạn" (expired) error instead of "tạm ngưng" (suspended) |
| **BUG-05** | Return overdue | Returning overdue book shows no warning/penalty notification |
| **BUG-06** | Return (authorization) | Member can return another member's book |
| **BUG-12** | Slip lookup | Member can look up another member's private borrow slip records |

---

## 5. System Quality Assessment

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| **Functional Integrity** | ❌ LOW | Core constraints (borrow limit, member states) bypassed or incorrectly handled |
| **Input Validation** | ❌ LOW | Email validation logic broken — accepts invalid, rejects valid |
| **Usability & UX** | ⚠️ MEDIUM | Generic error messages make debugging impossible for librarians |
| **Security & Authorization** | ❌ LOW | Members can view/act on other members' records |
| **Real-time UI Updates** | ✅ HIGH | Book statuses update immediately without page reload |
| **Flutter Web Handling** | ✅ HIGH | Smart Wait (`wait_for_flutter`) used consistently — no `time.sleep` |

---

## 6. Textbook Concepts Applied

| Concept | Textbook Chapter | Application in This Repo |
|---------|-----------------|--------------------------|
| RIPR Model | Ch.2 | `[R]`, `[I]`, `[P]`, `[R✓]` comments in every test function |
| Data-Driven Testing | Ch.3 §3.3.2 | `@parametrize` in `test_login_fail_parametrized` (Bonus B2) |
| Test Oracle Strength | Ch.14 | Strong assertions checking specific text — not just URLs (Bonus B3) |
| Test Doubles (Mock/Stub) | Ch.12 | System uses in-memory mock — data resets on page reload |
| Flaky Test Prevention | Ch.4 §4.2 | `wait_for_flutter()` replaces `time.sleep()` throughout |

---

*This report was generated by STQA Group 05 — Semester 2 2025-2026*
