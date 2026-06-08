# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System
**System URL**: https://stqa.rbc.vn
**Tools**: Python + Playwright + pytest
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| Total test cases executed | **40** (TC-01 to TC-40) |
| Passed | **25** |
| Failed (confirmed system bugs) | **15** |
| Bugs detected & verified | **13** (BUG-01 to BUG-12 + BUG-AUTO-01) |

> **Execution environment**: Local (Linux, headed Chromium, Python 3.10).
> `pytest -v` — Full suite runtime: ~18–22 minutes (extensive validation and smart waits on Flutter CanvasKit).
> Results: **25 passed, 15 failed** (15 FAILED = confirmed system bugs / security violations).

---

## 2. Test Case Details

### Group 1: Login — REQ-01 (test_login.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-01 | Successful login as Librarian | ✅ PASS | Librarian home screen with "Đăng xuất" confirmed |
| TC-02 | Successful login as Member | ✅ PASS | Member home screen with "Đăng xuất" confirmed |
| TC-03 | Failed login — email does not exist | ✅ PASS | "Không tìm thấy" error shown |
| TC-04 | Failed login — wrong password | ✅ PASS | "Mật khẩu không đúng" error shown |
| TC-05 | Failed login — both fields empty | ✅ PASS | "Vui lòng nhập..." validation shown |
| TC-06 | Failed login — email empty, password filled | ❌ FAIL | **BUG-01**: Shows generic "Vui lòng nhập email và mật khẩu" instead of specific "Vui lòng nhập email" |
| TC-07 | Failed login — email filled, password empty | ❌ FAIL | **BUG-02**: Shows generic "Vui lòng nhập email và mật khẩu" instead of specific "Vui lòng nhập mật khẩu" |

### Group 2: View Books — REQ-02 (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-08 | View all books display by list (20 books) | ✅ PASS | All book cards present with required fields |
| TC-09 | Book status updates real-time after borrow | ✅ PASS | Status changes to "Đang mượn" immediately |
| TC-10 | Book status updates real-time after return | ✅ PASS | Status reverts to "Có sẵn" immediately |
| TC-11 | BOOK001 displays full information | ✅ PASS | Title, author, genre, year, code, status all present |

### Group 3: Search & Filter — REQ-03 (test_search.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-12 | Search books by title "Flutter" | ✅ PASS | BOOK001 displayed correctly |
| TC-13 | Search books by author "Nguyễn Minh Đức" | ✅ PASS | BOOK001, BOOK009 displayed |
| TC-14 | Search by non-existent keyword "XYZ123" | ✅ PASS | "Không tìm thấy" message shown |
| TC-15 | Search is case-insensitive (FLUTTER vs flutter) | ❌ FAIL | **BUG-AUTO-01**: System is case-sensitive; "FLUTTER" returns no results |
| TC-16 | Filter books by genre "Kinh tế" | ✅ PASS | Only "Kinh tế" books are displayed |
| TC-17 | Filter by non-existent genre "Tâm lý học" | ✅ PASS | "Không tìm thấy" message shown |

### Group 4: Borrow Book — REQ-04 (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-18 | Active member borrows available book successfully | ✅ PASS | Success notification and borrow record created |
| TC-19 | Cannot borrow an already borrowed book | ✅ PASS | "Mượn sách này" button hidden after borrow |
| TC-20 | Cannot borrow a lost book | ✅ PASS | "Mượn sách này" button absent on lost book |
| TC-21 | Suspended member cannot borrow | ❌ FAIL | **BUG-04**: Rejects correctly but shows expired-account message ("hết hạn") instead of suspended warning |
| TC-22 | Expired member cannot borrow | ✅ PASS | "hết hạn" error shown correctly |
| TC-23 | Cannot borrow more than 3 books | ❌ FAIL | **BUG-03**: System allows borrowing a 4th book beyond the 3-book limit |

### Group 5: Return Book — REQ-05 (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-24 | Return book on time successfully | ✅ PASS | No overdue warning shown, status reverts to "Có sẵn" |
| TC-25 | Return book on due date — shows overdue warning | ❌ FAIL | **BUG-05**: No overdue warning displayed upon return |
| TC-26 | Return overdue book — shows overdue warning | ❌ FAIL | **BUG-05**: No overdue warning displayed upon return |
| TC-27 | Member cannot return another member's book | ❌ FAIL | **BUG-06**: System allows returning another member's book without authorization |

### Group 6: Overdue Handling — REQ-06 (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-28 | Librarian checks and views overdue books | ✅ PASS | "Đã cập nhật" and "Quá hạn" statuses confirmed |
| TC-29 | Member views their own overdue slips | ✅ PASS | MEM002 sees BR001 with overdue status |

### Group 7: Member Management — REQ-07 (test_member_management.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-30 | View member detailed information | ✅ PASS | Name, ID, email, phone, status all displayed |
| TC-31 | Add valid member successfully | ❌ FAIL | **BUG-07**: Valid email flagged as "Invalid email" and rejected |
| TC-32 | Reject member with invalid email format | ❌ FAIL | **BUG-08**: Invalid email "new@gmail" accepted and member is created |
| TC-33 | Reject member with duplicate email | ❌ FAIL | **BUG-09**: Shows generic "Invalid email" instead of duplicate email error |
| TC-34 | Reject member with empty full name | ✅ PASS | Validation warning shown correctly |
| TC-35 | Reject member with empty phone number | ❌ FAIL | **BUG-10**: Shows "Invalid email" error instead of phone validation error |
| TC-36 | Reject member with invalid phone format | ❌ FAIL | **BUG-11**: Shows "Invalid email" error instead of phone format error |

### Group 8: Borrow Record Lookup — REQ-08 (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-37 | Member can only view their own borrow records | ❌ FAIL | **BUG-12**: Member can view another member's records (security violation) |
| TC-38 | Librarian can view all borrow records | ✅ PASS | All member records visible to Librarian |
| TC-39 | Member cannot look up another member's slip | ❌ FAIL | **BUG-12**: Lookup returns another member's private borrow details |
| TC-40 | Borrow record displays full information | ✅ PASS | Record ID, title, borrow date, due date, status all present |

---

## 3. Bugs Detected during Automated Testing

The automated test suite has successfully verified and confirmed **13 bugs** in the system (BUG-01 to BUG-12 + BUG-AUTO-01).

### 3.1. Login Bugs (REQ-01)
* **BUG-01** (TC-06): When only the email field is empty, login shows generic "Vui lòng nhập email và mật khẩu" instead of "Vui lòng nhập email".
* **BUG-02** (TC-07): When only the password field is empty, login shows generic "Vui lòng nhập email và mật khẩu" instead of "Vui lòng nhập mật khẩu".

### 3.2. Search & Filter Bugs (REQ-03)
* **BUG-AUTO-01** (TC-15): Book search is case-sensitive; searching "FLUTTER" returns zero results while "Flutter" works correctly. This violates REQ-03.

### 3.3. Borrow Book Bugs (REQ-04)
* **BUG-03** (TC-23): The system allows a member to successfully borrow more than 3 books, violating the 3-book borrowing limit.
* **BUG-04** (TC-21): Borrowing with a suspended account (`cu.le@email.com`) correctly rejects but triggers an "account expired" message ("hết hạn") instead of the correct "account suspended" message ("tạm ngưng").

### 3.4. Return Book Bugs (REQ-05)
* **BUG-05** (TC-25, TC-26): Returning an overdue book or a book returned on its due date does not display any overdue warning/penalty notification.
* **BUG-06** (TC-27): A member can return another member's book by looking up their member ID in the slip lookup and clicking "Trả sách".

### 3.5. Member Management Bugs (REQ-07)
* **BUG-07** (TC-31): Adding a member with a perfectly valid email format (e.g. `testnewuser99@gmail.com`) fails with "Email không hợp lệ".
* **BUG-08** (TC-32): Adding a member with an invalid email format (e.g. `new@gmail`, missing domain extension) is accepted successfully.
* **BUG-09** (TC-33): Registering with a duplicate email shows a generic "Email không hợp lệ" instead of a duplicate entry error.
* **BUG-10** (TC-35): Registering with an empty phone number shows "Email không hợp lệ" instead of a phone field validation error.
* **BUG-11** (TC-36): Registering with an invalid phone format (e.g. letters) shows "Email không hợp lệ" instead of a phone format error.

### 3.6. Borrow Record Lookup Bugs (REQ-08)
* **BUG-12** (TC-37, TC-39): Members can perform unauthorized lookups on other members' borrow slips, exposing private borrow records. This is a critical security vulnerability.

---

## 4. Evaluation and System Quality Assessment

The system handles standard happy-path flows correctly but suffers from critical logic flaws, input validation gaps, and security vulnerabilities.

### Key Issues:
1. **Validation Masking**: Nearly all member management validation errors (empty phone, invalid phone, duplicate email, even valid email) are masked behind a generic "Email không hợp lệ" message. This makes troubleshooting impossible for librarians.
2. **Security Vulnerabilities**: Members can view and act upon other members' borrow records without authorization, violating data privacy and transaction integrity.
3. **Business Rule Violations**: The 3-book borrowing limit is not enforced. Suspended/expired member states are confused in error messaging.
4. **Overdue Warning Missing**: The system silently accepts overdue book returns without alerting staff or members, undermining library policy enforcement.

### Quality Assessment Summary

| Dimension | Rating | Justification |
|-----------|--------|---------------|
| Functional Integrity | ❌ LOW | Core constraints (borrow limits, member states) are bypassed or incorrectly handled |
| Input Validation | ❌ LOW | Multiple form fields accept invalid data or reject valid input (email validation logic) |
| Usability & UX | ⚠️ MEDIUM | Generic and misleading error messages for login and registration reduce usability |
| Security & Authorization | ❌ LOW | Information disclosure and unauthorized write operations are possible by any member |
| Real-time UI Updates | ✅ HIGH | Book and borrow statuses update immediately in the UI without page reload |

---

*This report was generated by STQA Group 05 — Semester 2 2025-2026*
