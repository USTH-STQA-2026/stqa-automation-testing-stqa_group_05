# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System
**System URL**: https://stqa.rbc.vn
**Tools**: Python + Playwright + pytest
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| Total test cases executed | 12 (mandatory TC-01→TC-12) + 2 (Bonus B1 extra TCs) + 3 (Bonus B2 parametrized) = **17** |
| Passed (local run) | **16** |
| Failed (confirmed system bug) | **1** (BUG-AUTO-01) |
| Bugs directly detected by automation | 1 |
| Bugs referenced from Manual Testing A1 | 2 (BUG-REF-01, BUG-REF-02) |

> **Execution environment**: Local (Windows, headed Chromium, Python 3.13).
> `pytest -v --tb=short` — Full suite runtime: ~3m 30s.
> Results: **16 passed, 1 failed** (1 FAIL = confirmed system bug REQ-03 violation).

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

### Group 2: Search & Filter (test_search.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-04 | Search by title "Flutter" | ✅ PASS | BOOK001 displayed correctly |
| TC-05 | Search with no results | ✅ PASS | "Không tìm thấy" message displayed |
| TC-06 | Filter by category "Công nghệ" | ✅ PASS | All displayed books belong to Technology category |
| TC-07 | Search by author "Nguyễn Minh Đức" | ✅ PASS | BOOK001, BOOK009 displayed |
| TC-Bonus-02 (B1) | Case-insensitive search | ❌ FAIL | **BUG-AUTO-01**: System is case-sensitive — REQ-03 violation |

### Group 3: Borrow & Return (test_borrow_return.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-08 | Borrow an available book | ✅ PASS | Book status changes to "Đang mượn" |
| TC-09 | View borrowed books list | ✅ PASS | MEM002 sees BR001 (BOOK003) from seed data |
| TC-10 | Return a borrowed book | ✅ PASS | Success notification confirmed, status updates to "Đã trả" |

### Group 4: General Functions (test_general.py)

| TC | Description | Result | Notes |
|----|-------------|--------|-------|
| TC-11 | Logout | ✅ PASS | Returns to login page, "Đăng xuất" button disappears |
| TC-12 | Switch language to English | ✅ PASS | UI switches to English: "Sign out", "Borrow this book", "Library" confirmed |

---

## 3. Bugs Detected during Automated Testing

### 3.1. Bugs Directly Detected by This Automation Suite

#### BUG-AUTO-01: Search is case-sensitive — violates REQ-03

- **Detected by**: TC-Bonus-02 (`test_search_case_insensitive`) — **FAIL**
- **Severity**: Medium
- **Steps to reproduce**: Log in → type `"FLUTTER"` (all uppercase) in search bar → system returns **no results**
- **Expected behavior (REQ-03)**: Search must be case-insensitive; `"FLUTTER"` should return the same results as `"Flutter"`
- **Actual behavior**: System performs exact-match search. Searching `"FLUTTER"` returns no book cards.
- **Evidence**: `AssertionError: assert 'Flutter' in sem_text` failed

> **Note on TC-12 (was previously reported as FAIL — now PASS)**:
> The original test asserted for the keyword `"Logout"` which was assumed to be the English
> translation of `"Đăng xuất"`. A diagnostic investigation revealed this was a **Test Oracle Error**
> (wrong expected value), NOT a system bug. The app actually uses **`"Sign out"`** as the English
> button label. After correcting the assertion, TC-12 passed immediately with a 10s timeout.
> The language switch works correctly — the flt-semantics tree updates synchronously.

### 3.2. Additional Bugs — Referenced from Manual Testing A1

> These bugs were originally discovered during manual testing (Assignment A1).
> The current automated test scenarios do not exercise the exact conditions required to trigger them.

#### BUG-REF-01: System allows borrowing books beyond the limit of 3 (REQ-04)

- **Associated TC**: TC-08 (tests basic borrow — does not reach the limit)
- **Severity**: High
- **Description**: When a user already has 3 active loans, the system still allows borrowing more. The borrow limit check is absent.
- **Source**: Manual Testing A1 — BUG-001

#### BUG-REF-02: Returning an overdue book does not trigger a warning (REQ-05)

- **Associated TC**: TC-10 (asserts return success only — does not check for overdue warning)
- **Severity**: Medium
- **Description**: System returns the book successfully but shows `"Trả sách thành công."` without overdue notice.
- **Source**: Manual Testing A1 — BUG-006

---

## 4. Evaluation and System Quality Assessment

### 4.1. Fully Functional Features (verified by automation)

| Feature | REQ | Result |
|---------|-----|--------|
| Login with valid credentials | REQ-01 | ✅ Works correctly |
| Login error messages | REQ-01 | ✅ "Mật khẩu không đúng", "Vui lòng nhập" shown correctly |
| Empty field validation | REQ-01 | ✅ Validation fires on submit |
| Librarian role privileges | REQ-07 | ✅ "Thêm thành viên", "Đặt lại dữ liệu" exclusive to Librarians |
| Search by title | REQ-03 | ✅ Works (lowercase input) |
| Search by author | REQ-03 | ✅ Works |
| Search — no results | REQ-03 | ✅ "Không tìm thấy" message shown |
| Filter by category | REQ-03 | ✅ Only matching books shown |
| Borrow available book | REQ-04 | ✅ Status updates to "Đang mượn" |
| View borrowed books list | REQ-04 | ✅ Active loans visible in "Mượn / Trả" tab |
| Return borrowed book | REQ-05 | ✅ Success confirmed |
| Logout | REQ-01 | ✅ Returns to login page, session cleared |

### 4.2. Bugs Found (confirmed by automation)

| Bug | Severity | REQ Violated | Detected By |
|-----|----------|-------------|-------------|
| Search case-sensitive (FLUTTER vs Flutter) | Medium | REQ-03 | TC-Bonus-02 (FAIL) |
| Borrow limit not enforced (>3 books) | High | REQ-04 | Manual A1 (BUG-001) |
| Overdue return has no warning | Medium | REQ-05 | Manual A1 (BUG-006) |

### 4.3. Conclusion

The system is stable for **read-only and standard transactional operations** (login, search, borrow, return, logout, language switch). All 12 mandatory test cases run and produce meaningful results. **1 bug was directly caught by automation** (case-sensitive search violates REQ-03). Two additional high/medium bugs from manual testing were cross-referenced. TC-12 (language switch) initially failed due to a Test Oracle Error in the assertion — after investigation and correction, it now passes.

---

## 5. Bonus Features Implemented

| Bonus | Description | Implemented |
|-------|-------------|-------------|
| B1 | ≥3 extra test cases | ✅ TC-Extra-01 (Librarian login), TC-Extra-02 (case-insensitive search), TC-Extra-03 (data-driven login failures) |
| B2 | Data-driven test with `@pytest.mark.parametrize` | ✅ `test_login_fail_parametrized` — 3 datasets |
| B3 | Detailed assertions (text, state, not just URL) | ✅ All TCs check semantics text content and negative conditions |
| B4 | `REPORT.md` with descriptions and analysis | ✅ This document |

---

## 6. AI Usage Declaration

- The group utilized **AI (ChatGPT)** to assist in writing automated test scripts and fixing test assertions.
- Specifically:
  - AI suggested Playwright selectors compatible with Flutter Web (CanvasKit) semantics tree.
  - AI structured RIPR Model comments and Arrange-Act-Assert flow in each test.
  - AI identified and fixed incorrect assertion in `test_login_as_librarian` (checking for actual UI labels "Thêm thành viên"/"Đặt lại dữ liệu" instead of non-existent "Thành viên" tab).
  - AI investigated TC-12 failure and corrected the assertion ("Logout" → "Sign out") to make TC-12 PASS.
- All test execution, bug analysis, and final quality assessments were reviewed and confirmed by the group.
- Code was reviewed and understood before submission.

---

*This report was generated by STQA Group 05 — Semester 2 2025-2026*
