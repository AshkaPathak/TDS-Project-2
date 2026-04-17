# Project 2 — Q1: Crack the Gate 1

## Problem Summary

The challenge provided a login portal for a known user:

Email: ctf-player@picoctf.org

The description clearly stated that password guessing would not work and hinted that the developer may have left a secret way into the system. This suggested that the solution involved finding a hidden authentication bypass rather than brute forcing credentials.

---

## Step 1 — Launch the picoCTF Instance

The instance was launched from the picoCTF assignment page. Once the status changed to RUNNING, the challenge website became accessible through the provided link.

---

## Step 2 — Inspect the Login Page Source

The login page contained a simple HTML form with email and password fields. The form submission was handled using JavaScript with a fetch request to /login.

While inspecting the HTML source, the following hidden comment was discovered:

ABGR: Wnpx - grzcbenel olcnff: hfr urnqre "K-Qri-Npprff: lrf"

This comment looked suspicious and was clearly not meant for users.

---

## Step 3 — Decode the Hidden Comment

The text was encoded using ROT13.

Decoding it gives:

NOTE: Jack - temporary bypass: use header "X-Dev-Access: yes"

This revealed a hidden developer backdoor. The backend allows authentication if the request contains the header:

X-Dev-Access: yes

---

## Step 4 — Verify Normal Login Failure

Attempting to log in normally using:

Email: ctf-player@picoctf.org  
Password: any value

resulted in a 401 Unauthorized response. This confirmed that standard login would not work.

---

## Step 5 — Send a Modified Request from the Browser Console

Since the login form does not allow adding custom headers, the request was manually crafted using the browser console.

The following JavaScript code was executed:

fetch('/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Dev-Access': 'yes'
  },
  body: JSON.stringify({
    email: 'ctf-player@picoctf.org',
    password: '123'
  })
})
.then(response => response.json())
.then(data => {
  console.log(data);
  alert(JSON.stringify(data));
});

---

## Step 6 — Capture the Server Response

The server responded successfully with the flag:

picoCTF{brut4_f0rc4_125f752d}

---

## Final Flag

picoCTF{brut4_f0rc4_125f752d}

---

## Why This Worked

The application contained a hidden developer bypass left in production code. This bypass required a custom HTTP header to be included in the request.

The header:

X-Dev-Access: yes

allowed the backend to skip authentication and directly return a successful response containing the flag.

---

## Conclusion

The challenge was solved by:

1. Launching the instance  
2. Inspecting the login page source  
3. Finding a hidden ROT13-encoded comment  
4. Decoding it to reveal a developer bypass header  
5. Sending a crafted request with the required header  
6. Extracting the flag from the response  

Final result:

Authentication bypass achieved and flag successfully retrieved without brute force.
