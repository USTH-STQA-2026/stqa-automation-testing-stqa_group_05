# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System
**System URL**: https://stqa.rbc.vn
**Tools**: Python + Playwright + pytest
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| Total test cases executed | 12 (mandatory) + 2 (Bonus B1) + 3 (Bonus B2 parametrized) = 17 |
| Passed test cases | 14 |
| Failed test cases (detected bugs) | 3 |
| Bugs directly detected by automation | 2 (BUG-AUTO-01, BUG-AUTO-02) |
| Bugs referenced from Manual Testing A1 | 2 (BUG-REF-01, BUG-REF-02) |

> Note: Bonus B2 uses `@pytest.mark.parametrize` with 3 datasets, which pytest automatically expands and executes as 3 separate test runs. Actual results are obtained from running `pytest -v`.

---

## 2. Test Case Details

### Group 1: Login (test_login.py)

| TC | Description | Actual Result | Notes |
|----|-------------|---------------|-------|
| TC-01 | Successful login (User MEM002) | PASS | Starter template example |
| TC-02 | Failed login — incorrect password | PASS | Correctly shows "Mật khẩu không đúng" (Wrong password) |
| TC-03 | Failed login — both fields empty | PASS | Correctly shows "Vui lòng nhập..." (Please enter...) |
| TC-Bonus-01 (B1) | Librarian login — privilege verification | FAIL | Bug: Assertion `"Thành viên" in sem_text` failed — system shows "Thêm thành viên" button, not a standalone "Thành viên" tab label (REQ-07 label mismatch) |
| TC-Bonus-B2a | Data-driven: incorrect password | PASS | |
| TC-Bonus-B2b | Data-driven: empty fields | PASS | |
| TC-Bonus-B2c | Data-driven: email does not exist | PASS | |

### Group 2: Search & Filter (test_search.py)

| TC | Description | Actual Result | Notes |
|----|-------------|---------------|-------|
| TC-04 | Search by title "Flutter" | PASS | BOOK001 displayed correctly |
| TC-05 | Search with no results | PASS | "Không tìm thấy" (Not found) message displayed, no book cards shown |
| TC-06 | Filter by category "Công nghệ" (Technology) | PASS | All displayed books belong to Technology category |
| TC-07 | Search by author "Nguyễn Minh Đức" | PASS | BOOK001, BOOK009 displayed |
| TC-Bonus-02 (B1) | Case-insensitive search | FAIL | Bug: Search is case-sensitive (searching "FLUTTER" returns no results) |

### Group 3: Borrow & Return (test_borrow_return.py)

| TC | Description | Actual Result | Notes |
|----|-------------|---------------|-------|
| TC-08 | Borrow an available book | PASS | Book status changes to "Đang mượn" (Borrowed) |
| TC-09 | View borrowed books list | PASS | MEM002 successfully sees BR001 in seed data |
| TC-10 | Return a borrowed book | PASS | Book status reverts to "Có sẵn" (Available) |

### Group 4: General Functions (test_general.py)

| TC | Description | Actual Result | Notes |
|----|-------------|---------------|-------|
| TC-11 | Logout | PASS | Returns to login page |
| TC-12 | Switch language to EN | FAIL | TimeoutError: "Logout" text did not appear after clicking "EN" |

---

## 3. Bugs Detected during Automated Testing

### 3.1. Bugs Directly Detected by This Automation Suite

#### BUG-AUTO-01: Search is case-sensitive — violates REQ-03

- **Detected by**: TC-Bonus-02 (`test_search_case_insensitive`) — **FAIL**
- **Severity**: Medium
- **Steps to reproduce**: Log in → search for `"FLUTTER"` (uppercase) → system returns **no results**
- **Expected behavior (REQ-03)**: Search must be case-insensitive; searching `"FLUTTER"` should return the same results as `"Flutter"`
- **Actual behavior**: System performs exact-match search. No results returned for uppercase input.
- **Evidence**: AssertionError — `assert 'Flutter' in sem_text` failed when input was `"FLUTTER"`

#### BUG-AUTO-02: Language switch to EN does not re-render UI within timeout — violates REQ

- **Detected by**: TC-12 (`test_switch_language_to_english`) — **FAIL** (both local and CI)
- **Severity**: Medium
- **Steps to reproduce**: Log in → click `"EN"` button → wait for UI to update
- **Expected behavior**: All UI labels should switch to English (e.g., `"Logout"`, `"Borrow"`)
- **Actual behavior**: After clicking `"EN"`, the keyword `"Logout"` does not appear in the Semantics Tree within 10 seconds. UI labels remain in Vietnamese or the semantics tree is not updated in time.
- **Evidence**: TimeoutError — `Locator.wait_for: Timeout 10000ms exceeded` waiting for text `"Logout"`

---

### 3.2. Additional Bugs — Referenced from Manual Testing A1

> These bugs were originally discovered during manual testing (Assignment A1).
> The current automated test scenarios (TC-08, TC-10) do not exercise the exact conditions
> required to trigger them, so they are not directly caught by this automation suite.
> They are included here for completeness.

#### BUG-REF-01: System allows borrowing books beyond the limit of 3 (REQ-04)

- **Associated TC**: TC-08 (only tests basic borrow with 1 book — does not reach the limit)
- **Severity**: High
- **Description**: When a user already has 3 active loans, the system still allows borrowing more. The check for `currentBorrowedBooksCount >= 3` is missing.
- **Source**: Documented in Manual Testing A1 (BUG-001)

#### BUG-REF-02: Returning an overdue book does not trigger a warning (REQ-05)

- **Associated TC**: TC-10 (only asserts return success — does not check for overdue warning)
- **Severity**: Medium
- **Description**: The system returns the book successfully but does not display an overdue warning. The message shows `"Trả sách thành công."` instead of including the overdue notice.
- **Source**: Documented in Manual Testing A1 (BUG-006)


---

## 4. Evaluation and System Quality Assessment

### 4.1. Fully Functional Features
- **Login / Logout**: Smooth execution, accurate error messages, and correct input validation.
- **Search & Filter**: Works correctly according to REQ-03, except for the case-insensitivity bug.
- **Real-time Status Updates**: Book statuses are updated immediately upon successful borrow/return actions.
- **Privilege Separation**: Librarian account logs in successfully and has special actions ("Thêm thành viên", "Đặt lại dữ liệu") not available to regular members. However, the exact label "Thành viên" expected by TC-Bonus-01 was not found — assertion needs refinement.
- **Language Switching**: Feature exists in the UI ("EN" button is clickable), but TC-12 FAILED on the CI environment with a timeout — the "Logout" keyword did not appear within 10 seconds after switching language.

### 4.2. Existing Bugs (Identified in Manual Testing A1)
- **REQ-04**: Fails to block borrowing beyond 3 books (BUG-001 — High).
- **REQ-04**: Displays incorrect error message when a suspended user attempts to borrow (BUG-002 — Medium).
- **REQ-05**: Overdue returns do not trigger warnings (BUG-006 — Medium).
- **REQ-07**: Email validation logic is inverted — accepts invalid emails and rejects valid ones (BUG-003 — Critical).
- **REQ-08**: Members can search and return books belonging to other members (BUG-004, BUG-005 — Critical).

### 4.3. Conclusion
The system runs stably for read-only actions (viewing, searching, logging in). However, transactional write actions (borrowing, member management, loan permission checks) contain critical logical bugs that need to be addressed immediately.

---

## 5. AI Usage Declaration

- The group utilized AI (ChatGPT) to assist in writing the automated test scripts.
- Specifically, the AI suggested Playwright selectors compatible with Flutter Web (CanvasKit), the structure of the RIPR Model in comments, and how to utilize `wait_for_flutter` instead of `time.sleep`.
- The group reviewed, understood, and modified the AI-generated code before deployment.
- All analysis of test execution results, bug reporting, and final quality assessments were completed solely by the group members.

---

*This report was generated by STQA Group 05 — Semester 2 2025-2026*
