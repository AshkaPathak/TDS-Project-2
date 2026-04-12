# Project 2 — Q3: Power Cookie (Privilege Escalation via Cookies)

## Problem Summary
The challenge provides a web application (Online Gradebook) with a "Continue as guest" option. Upon accessing as a guest, the application displays:

"We apologize, but we have no guest services at the moment."

The objective is to analyze the application and retrieve the hidden flag.

---

## Initial Observations
- The application does not allow guest access.
- No visible login form or input fields.
- The response suggests access control based on user roles.
- This indicates that authentication or authorization may be handled client-side.

---

## Key Insight
Modern web applications often use cookies to store session or role information.

If the server trusts cookie values without validation, it becomes vulnerable to **privilege escalation attacks**.

---

## Step-by-Step Solution

### Step 1 — Open Developer Tools
Open browser developer tools:

Mac:
Cmd + Option + I

Navigate to:
Storage / Application → Cookies

---

### Step 2 — Inspect Cookies
Under the domain:

saturn.picoctf.net

A cookie was found:

Name:
isAdmin

Value:
0

---

### Step 3 — Analyze Cookie Purpose
The cookie name `isAdmin` clearly indicates role-based access control.

Value interpretation:
- 0 → Not admin (guest/user)
- 1 → Admin

---

### Step 4 — Modify Cookie
Change the cookie value:

Before:
isAdmin = 0

After:
isAdmin = 1

Press Enter to apply the change.

---

### Step 5 — Refresh the Page
Reload the page after modifying the cookie.

---

## Result
After refreshing, the application grants admin-level access and reveals the flag:

picoCTF{gr4d3_A_c00k13_65fd1e1a}

---

## Why This Worked
The server relied entirely on a client-side cookie (`isAdmin`) to determine user privileges.

There was:
- No server-side validation
- No signing or encryption of cookies
- No session verification

This allowed direct privilege escalation by modifying the cookie value.

---

## Security Insight
This is a classic example of **Insecure Direct Trust of Client Input**.

Secure implementations should:
- Use server-side sessions
- Sign cookies (e.g., JWT with signature)
- Validate roles on the backend

---

## Final Answer
picoCTF{gr4d3_A_c00k13_65fd1e1a}
