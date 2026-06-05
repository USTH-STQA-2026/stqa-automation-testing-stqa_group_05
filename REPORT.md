# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System
**System URL**: https://stqa.rbc.vn
**Tools**: Python + Playwright + pytest
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| Total test cases executed | **29** (16 standard/bonus tests + 13 bug-detection tests) |
| Passed (local run) | **16** |
| Failed (confirmed system bugs) | **13** (12 manual testing bugs + 1 automated search bug) |
| Bugs directly detected & verified | **13** |

> **Execution environment**: Local (Linux, headed/headless Chromium, Python 3.10).
> `pytest -v` — Full suite runtime: ~14 minutes (due to extensive validation and smart waits on Flutter CanvasKit).
> Results: **16 passed, 13 failed** (13 FAILED = confirmed system bugs / security violations).

---

## 2. Test Case Details

### Group 1: Login (test_login.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-01 | Successful login (User MEM002) | ✅ PASS | Starter template example — RIPR model demonstrated |
| TC-02 | Failed login — incorrect password | ✅ PASS | Correctly shows "Mật khẩu không đúng" |
| TC-03 | Failed login — both fields empty | ✅ PASS | Correctly shows "Vui lòng nhập..." |
| TC-Bonus-01 (B1) | Librarian login — privilege verification | ✅ PASS | Asserts "Thêm thành viên" / "Đặt lại dữ liệu" buttons (REQ-07 exclusive to Librarians) |
| TC-Bonus-B2a | Data-driven: incorrect password | ✅ PASS | `@parametrize` — email ba.nguyen, wrong password |
| TC-Bonus-B2b | Data-driven: empty fields | ✅ PASS | `@parametrize` — both fields empty |
| TC-Bonus-B2c | Data-driven: email does not exist | ✅ PASS | `@parametrize` — nobody@test.com |
| TC-06 | Failed login — empty email only | ❌ FAIL | **BUG-01**: Displays generic "Vui lòng nhập email và mật khẩu" instead of specific email warning |
| TC-07 | Failed login — empty password only | ❌ FAIL | **BUG-02**: Displays generic "Vui lòng nhập email và mật khẩu" instead of specific password warning |

### Group 2: Search & Filter (test_search.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-04 | Search by title "Flutter" | ✅ PASS | BOOK001 displayed correctly |
| TC-05 | Search with no results | ✅ PASS | "Không tìm thấy" message displayed |
| TC-06 | Filter by category "Công nghệ" | ✅ PASS | All displayed books belong to Technology category |
| TC-07 | Search by author "Nguyễn Minh Đức" | ✅ PASS | BOOK001, BOOK009 displayed |
| TC-Bonus-02 (B1) | Case-insensitive search | ❌ FAIL | **BUG-AUTO-01**: System is case-sensitive — REQ-03 violation (e.g. "FLUTTER" returns no results) |

### Group 3: Borrow & Return (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-08 | Borrow an available book | ✅ PASS | Book status changes to "Đang mượn" |
| TC-09 | View borrowed books list | ✅ PASS | MEM002 sees BR001 (BOOK003) from seed data |
| TC-10 | Return a borrowed book | ✅ PASS | Success notification confirmed, status updates to "Đã trả" |
| TC-18 | Suspended member cannot borrow | ❌ FAIL | **BUG-03**: Rejects but displays expired-account message ("hết hạn") instead of suspended-account warning |
| TC-20 | Member borrow limit (max 3 books) | ❌ FAIL | **BUG-04**: System allows member to borrow a 4th book successfully |
| TC-22 | Return overdue book displays warning | ❌ FAIL | **BUG-05**: Book returned successfully but no overdue warning is displayed |
| TC-23 | Cannot return another member's book | ❌ FAIL | **BUG-06**: Successfully allows a member to return a book borrowed by another member |
| TC-33 | Member cannot lookup other's slip | ❌ FAIL | **BUG-12**: Security violation — members can lookup and view details of another member's borrow slip |

### Group 4: General Functions (test_general.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-11 | Logout | ✅ PASS | Returns to login page, "Đăng xuất" button disappears |
| TC-12 | Switch language to English | ✅ PASS | UI switches to English: "Sign out", "Borrow this book", "Library" confirmed |

### Group 5: Member Management (test_member_management.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-25 | Add valid member successfully | ❌ FAIL | **BUG-07**: Valid email registered as member shows "Email không hợp lệ" and rejects |
| TC-26 | Reject invalid email format | ❌ FAIL | **BUG-08**: System accepts invalid email format "new@gmail" and adds member |
| TC-27 | Reject duplicate email | ❌ FAIL | **BUG-09**: Shows general "Email không hợp lệ" instead of duplicate email error |
| TC-29 | Reject empty phone number | ❌ FAIL | **BUG-10**: Shows general "Email không hợp lệ" instead of phone validation error |
| TC-30 | Reject invalid phone number format | ❌ FAIL | **BUG-11**: Shows general "Email không hợp lệ" instead of phone format error |

---

## 3. Bugs Detected during Automated Testing

The automated test suite has successfully verified and caught all 13 bugs in the system.

### 3.1. Login Bugs
* **BUG-01 (TC-06)**: Empty email login shows generic message "Vui lòng nhập email và mật khẩu".
* **BUG-02 (TC-07)**: Empty password login shows generic message "Vui lòng nhập email và mật khẩu".

### 3.2. Borrow & Return Bugs
* **BUG-03 (TC-18)**: Borrowing with a suspended account (`cu.le@email.com`) triggers an "account expired" error instead of "account suspended".
* **BUG-04 (TC-20)**: Borrow limit of 3 books is not enforced; a member can successfully borrow a 4th book.
* **BUG-05 (TC-22)**: Returning an overdue book does not display an overdue warning/penalty.
* **BUG-06 (TC-23)**: A member can return another member's book by looking up their member ID and clicking "Trả sách".
* **BUG-12 (TC-33)**: A member can perform unauthorized lookups on other members' borrowing slips, displaying private transaction details.

### 3.3. Member Management Bugs (Librarian)
* **BUG-07 (TC-25)**: Adding a member with a valid email (e.g. `testnewuser99@gmail.com`) fails with "Email không hợp lệ".
* **BUG-08 (TC-26)**: Adding a member with an invalid email format `new@gmail` (no domain extension) is accepted successfully.
* **BUG-09 (TC-27)**: Registering an already existing email shows a generic "Email không hợp lệ" error instead of a duplicate error.
* **BUG-10 (TC-29)**: Registering with an empty phone number shows a generic "Email không hợp lệ" instead of a phone validation error.
* **BUG-11 (TC-30)**: Registering with an invalid phone format (e.g. letters) shows a generic "Email không hợp lệ" instead of a phone format error.

### 3.4. Search & Filter Bugs
* **BUG-AUTO-01 (TC-Bonus-02)**: Book search is case-sensitive; searching "FLUTTER" yields zero results while "Flutter" works.

---

## 4. Evaluation and System Quality Assessment

The system functions correctly for standard, happy-path flows but suffers from critical logic flaws, lack of specific input validation, and security vulnerabilities:
1. **Validation Masking**: The member management form has a bug where almost all validation errors (empty phone, invalid phone, duplicate email, valid email) are masked behind a generic "Email không hợp lệ" error message, making troubleshooting impossible for librarians.
2. **Security Vulnerabilities**: Members can perform unauthorized queries on other members' records and perform writes (returning books) on behalf of other members.
3. **Business Rule Violations**: Borrowing limits (>3 books) are not enforced, and suspended/expired states are mixed up.

### Quality Assessment Summary
* **Functional Integrity**: ❌ LOW (Core constraints are bypassed or incorrectly handled).
* **Usability & UX**: ❌ MEDIUM (Confusing and incorrect error messages for login and registration).
* **Security & Authorization**: ❌ LOW (Information disclosure and unauthorized transaction state modifications are possible).

---

*This report was generated by STQA Group 05 — Semester 2 2025-2026*
