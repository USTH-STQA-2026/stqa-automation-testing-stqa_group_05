# REPORT.md — Automated Testing Execution Report

**Project**: Web UI Automation Testing — ABC Library Book Borrowing System  
**System URL**: https://stqa.rbc.vn  
**Tools**: Python + Playwright + pytest  
**Group**: STQA Group 05

---

## 1. Summary Statistics

| Category | Quantity |
|----------|----------|
| **Total test cases executed** | **28** (12 core TCs + 16 bonus TCs) |
| **Passed (local run)** | **16** (12 core TCs + 4 bonus TCs) |
| **Failed (confirmed system bugs)** | **12** (12 manual testing bugs) |
| **Total bugs detected & verified** | **12** (BUG-01 to BUG-12) |

> **Execution environment**: Local (Linux, headed Chromium, Python 3.10).  
> `pytest -v` — Full suite runtime: ~10 minutes.  
> Results: **16 passed, 12 failed** (12 FAIL = confirmed system bugs verified by automation).

---

## 2. Test Case Details

### Group 1: Login ([test_login.py](file:///home/hoang-vu/Documents/Usth/software_testing/stqa-automation-testing-stqa_group_05/tests/test_login.py))

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-01 | `test_login_success` | Successful login with valid credentials | ✅ PASS | `login_success.png` |
| TC-02 | `test_login_fail_wrong_password` | Failed login — incorrect password | ✅ PASS | `login_fail_wrong_password.png` |
| TC-03 | `test_login_fail_empty_fields` | Failed login — both fields empty | ✅ PASS | `login_fail_empty_fields.png` |
| TC-Bonus-01 (B1) | `test_login_as_librarian` | Librarian login — privilege verification | ✅ PASS | `login_librarian.png` |
| TC-Bonus-B2a | `test_login_fail_parametrized` | Data-driven: incorrect password | ✅ PASS | `login_fail_TC-02b.png` |
| TC-Bonus-B2b | `test_login_fail_parametrized` | Data-driven: empty fields | ✅ PASS | `login_fail_TC-03b.png` |
| TC-Bonus-B2c | `test_login_fail_parametrized` | Data-driven: email does not exist | ✅ PASS | `login_fail_TC-Login-Extra.png` |
| TC-Bonus-B1a | `test_login_fail_empty_email_only` | Empty email validation check | ❌ FAIL | `login_fail_empty_email_only.png` |
| TC-Bonus-B1b | `test_login_fail_empty_password_only` | Empty password validation check | ❌ FAIL | `login_fail_empty_password_only.png` |

*Note: TC-Bonus-B1a and TC-Bonus-B1b fail because they successfully detect **BUG-01** and **BUG-02** respectively.*

---

### Group 2: Search & Filter ([test_search.py](file:///home/hoang-vu/Documents/Usth/software_testing/stqa-automation-testing-stqa_group_05/tests/test_search.py))

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-04 | `test_search_book_by_name` | Search book by name/title | ✅ PASS | `search_by_name_flutter.png` |
| TC-05 | `test_search_book_no_result` | Search book — no results | ✅ PASS | `search_no_result.png` |
| TC-06 | `test_filter_by_category` | Filter books by category | ✅ PASS | `filter_by_category_cong_nghe.png` |
| TC-07 | `test_search_by_author` | Search book by author name | ✅ PASS | `search_by_author.png` |

---

### Group 3: Borrow & Return ([test_borrow_return.py](file:///home/hoang-vu/Documents/Usth/software_testing/stqa-automation-testing-stqa_group_05/tests/test_borrow_return.py))

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-08 | `test_borrow_book` | Borrow an available book | ✅ PASS | `borrow_book_success.png` |
| TC-09 | `test_view_borrowed_books` | View borrowed books list | ✅ PASS | `view_borrowed_books.png` |
| TC-10 | `test_return_book` | Return a borrowed book | ✅ PASS | `return_book_success.png` |
| TC-Bonus-B1c | `test_borrow_suspended_member` | Suspended member cannot borrow | ❌ FAIL | `borrow_suspended_member.png` |
| TC-Bonus-B1d | `test_borrow_limit_exceeded` | Cannot borrow more than 3 books | ❌ FAIL | `borrow_limit_exceeded.png` |
| TC-Bonus-B1e | `test_return_overdue_warning` | Overdue return triggers warning | ❌ FAIL | `return_overdue_warning.png` |
| TC-Bonus-B1f | `test_return_other_member_book` | Member return another member's book | ❌ FAIL | `return_other_member_book.png` |
| TC-Bonus-B1g | `test_unauthorized_slip_lookup` | Member lookup other member's slip | ❌ FAIL | `unauthorized_slip_lookup.png` |

*Note: These Bonus test cases fail because they successfully detect **BUG-04**, **BUG-03**, **BUG-05**, **BUG-06**, and **BUG-12** respectively.*

---

### Group 4: General Functions ([test_general.py](file:///home/hoang-vu/Documents/Usth/software_testing/stqa-automation-testing-stqa_group_05/tests/test_general.py))

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-11 | `test_logout` | Logout success | ✅ PASS | `logout_success.png` |
| TC-12 | `test_switch_language_to_english` | Switch language to English | ✅ PASS | `language_switched_to_english.png` |

---

### Group 5: Member Management ([test_member_management.py](file:///home/hoang-vu/Documents/Usth/software_testing/stqa-automation-testing-stqa_group_05/tests/test_member_management.py))

| TC | Test Function | Description | Result | Screenshot |
|----|--------------|-------------|--------|------------|
| TC-Bonus-B1h | `test_add_member_valid` | Librarian adds valid member | ❌ FAIL | `add_member_valid.png` |
| TC-Bonus-B1i | `test_add_member_invalid_email`| Reject invalid email format | ❌ FAIL | `add_member_invalid_email.png` |
| TC-Bonus-B1j | `test_add_member_duplicate_email`| Reject duplicate email | ❌ FAIL | `add_member_duplicate_email.png` |
| TC-Bonus-B1k | `test_add_member_empty_phone` | Reject empty phone number | ❌ FAIL | `add_member_empty_phone.png` |
| TC-Bonus-B1l | `test_add_member_invalid_phone`| Reject invalid phone format | ❌ FAIL | `add_member_invalid_phone.png` |

*Note: These Bonus test cases fail because they successfully detect **BUG-07**, **BUG-08**, **BUG-09**, **BUG-10**, and **BUG-11** respectively.*

---

## 3. Bugs Detected during Automated Testing

The automated test suite has successfully detected and verified **12 system bugs** (the complete list of bugs from manual testing):

### 3.1. Login Validation Bugs (REQ-01)

#### BUG-01: Empty email validation warning is generic
- **Detected by**: `test_login_fail_empty_email_only` (**FAIL**)
- **Description**: When only the Email field is empty and Password is provided, the system displays the generic message `"Vui lòng nhập email và mật khẩu"` instead of an email-specific message.
- **Evidence**: `login_fail_empty_email_only.png`

#### BUG-02: Empty password validation warning is generic
- **Detected by**: `test_login_fail_empty_password_only` (**FAIL**)
- **Description**: When only the Password field is empty and Email is provided, the system displays the generic message `"Vui lòng nhập email và mật khẩu"` instead of a password-specific message.
- **Evidence**: `login_fail_empty_password_only.png`

---

### 3.2. Borrow & Return Bugs (REQ-04, REQ-05, REQ-08)

#### BUG-03: Borrowing limit of 3 books is not enforced
- **Detected by**: `test_borrow_limit_exceeded` (**FAIL**)
- **Description**: An active member is allowed to borrow a 4th book successfully. The limit of 3 books is ignored.
- **Evidence**: `borrow_limit_exceeded.png`

#### BUG-04: Suspended member borrows with incorrect error message
- **Detected by**: `test_borrow_suspended_member` (**FAIL**)
- **Description**: When a suspended member attempts to borrow a book, the system displays `"Tài khoản thành viên đã hết hạn..."` (Expired) instead of the correct Suspended warning message.
- **Evidence**: `borrow_suspended_member.png`

#### BUG-05: Overdue book return has no overdue warning notice
- **Detected by**: `test_return_overdue_warning` (**FAIL**)
- **Description**: Returning an overdue borrowing slip completes successfully but displays only `"Trả sách thành công."` without any warning or overdue status indicator.
- **Evidence**: `return_overdue_warning.png`

#### BUG-06: Member can return another member's book
- **Detected by**: `test_return_other_member_book` (**FAIL**)
- **Description**: A member can look up another member's ID and click the return button, successfully returning their borrowed book.
- **Evidence**: `return_other_member_book.png`

#### BUG-12: Member can view another's borrowing slip
- **Detected by**: `test_unauthorized_slip_lookup` (**FAIL**)
- **Description**: A member can enter another member's ID in the search box under "Tra cứu phiếu mượn" and view their active borrowing slips, violating authorization rules.
- **Evidence**: `unauthorized_slip_lookup.png`

---

### 3.3. Member Management Bugs (REQ-07)

#### BUG-07: Valid email format is rejected during member creation
- **Detected by**: `test_add_member_valid` (**FAIL**)
- **Description**: The librarian cannot add a member with a valid email (e.g. `testnewuser99@gmail.com`), getting `"Invalid email"` error.
- **Evidence**: `add_member_valid.png`

#### BUG-08: Invalid email format is accepted during member creation
- **Detected by**: `test_add_member_invalid_email` (**FAIL**)
- **Description**: The librarian can successfully create a member with an invalid email format such as `new@gmail` (missing domain extension).
- **Evidence**: `add_member_invalid_email.png`

#### BUG-09: Duplicate email registration reports the wrong error
- **Detected by**: `test_add_member_duplicate_email` (**FAIL**)
- **Description**: Trying to add a member with an already-existing email (e.g., `librarian@library.com`) displays `"Invalid email"` instead of a duplicate error warning.
- **Evidence**: `add_member_duplicate_email.png`

#### BUG-10: Empty phone number registration reports the wrong error
- **Detected by**: `test_add_member_empty_phone` (**FAIL**)
- **Description**: Leaving the phone number field empty during member creation displays `"Invalid email"` instead of a phone validation error.
- **Evidence**: `add_member_empty_phone.png`

#### BUG-11: Invalid phone number format registration reports the wrong error
- **Detected by**: `test_add_member_invalid_phone` (**FAIL**)
- **Description**: Entering an invalid phone format (containing characters like `09abcde345`) displays `"Invalid email"` instead of a phone format validation error.
- **Evidence**: `add_member_invalid_phone.png`

---

## 4. Evaluation and System Quality Assessment

The system is highly functional for standard transactional flows (successful login, book viewing, successful borrowing of available books, returning on time, logging out, switching language). 

However, critical quality gaps exist in **validation logic, constraint enforcement, and access controls**:
- **Access Control & Authorization**: High-risk security vulnerabilities allow members to look up other members' borrowing slips (BUG-12) and return books on behalf of other members (BUG-06).
- **Constraint Enforcement**: The core business rule of limiting active loans to 3 books per member is not enforced (BUG-03).
- **Data Validation & Error Messaging**: Email validation is broken (accepts invalid format, rejects valid format, short-circuits phone validations) (BUG-07 to BUG-11). Validation alerts are generic and do not guide the user properly (BUG-01, BUG-02, BUG-04).
- **Overdue Handling**: No overdue warnings are shown upon returning overdue books (BUG-05).

---

## 5. Bonus Features Implemented

| Bonus | Description | Implementation Details |
|-------|-------------|------------------------|
| **B1** | ≥3 extra test cases | ✅ Implemented 16 extra tests covering all 12 manual bugs. |
| **B2** | Data-driven testing | ✅ Parameterized `test_login_fail_parametrized` with 3 failed login datasets (wrong password, empty fields, nonexistent email). |
| **B3** | Detailed assertions | ✅ Assertions check specific Vietnamese/English text content, verify correct status transitions, and enforce strict error messages. |
| **B4** | REPORT.md | ✅ Detailed execution report with descriptions, bug categorization, and quality assessment. |

---

## 6. AI Usage Declaration

The team utilized AI (Gemini/ChatGPT) to assist in writing test scripts and analyzing Playwright selectors compatible with Flutter Web semantics tree:
- AI helped identify the semantics selectors for the complex CanvasKit UI widgets.
- AI assisted in structuring tests using the Arrange-Act-Assert format and the textbook **RIPR Model**.
- AI aided in solving test flakiness by recommending Playwright's `wait_for` logic instead of hardcoded `time.sleep()`.

---
*This report was generated by STQA Group 05 — Semester 2 2025-2026*
