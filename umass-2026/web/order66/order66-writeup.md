# UMass 2026: web/order66

## Context & Vulnerability
This is an application with 66 order boxes and a link to the chancellor (admin) as well as a url 'logs for chancellor'. While testing out the site, you notice that you can only input into one of the orders. Additionally, regardless of the input, the link in the url box does not change, whereas inserting this link into the chancellor/admin does not work. The chancellor/admin also does not take https, only http connections.

In the code, you notice that is_payload_present variable hints at the XSS solve. 

`is_payload_present = "<script" in current_content.lower() or "alert(" in current_content.lower()`

Our goal is the flag which is in the admin's cookie (see app.js). Notice how secure is set to false meaning the browser will transmit this cookie over http connections which is what the chancellor/admin takes.

```
await page.setCookie({
    name: 'flag',
    value: FLAG,
    domain: parsedUrl.hostname,
    path: '/',
    httpOnly: false,
    secure: false,
    sameSite: 'Lax'
});
```

## Exploitation
We notice from the `hello_word()` function that there is one vulnerable index `current_vuln_index` that means one of the 66 boxes allows for XSS with javascript. 

```
if i == current_vuln_index and ("<script" in content.lower() or "alert(" in content.lower()):
    is_payload_present = True
```

Since we see that the index, uid, and seed don't change when we enter into the order boxes, we can test each box to see which one is vulnerable with `<script>alert(1)</script>` 

The box that allows the alert to go through is the vulnerable box which we can inject with a payload we want the chancellor/admin to execute. We can use `<script>console.log(document.cookie)</script>` in order to dump the cookie into the output of the chancellor/admin.

app.py also contains the endpoint `/view/<uid>/<int:seed>` which is what we want to add to the end of the ctf url to input to the chancellor/admin. Doing so dumps the flag.

```
◇ injecting env (0) from .env // tip: ⌘ override existing { override: true }
flag=UMASS{m@7_t53_f0rce_b$_w!th_y8u}
Failed to load resource: the server responded with a status of 404 (NOT FOUND)
```

## Remediation
The easiest remediation for this scenario in order for the user to be unable to access the cookie is setting secure equal to true since the chancellor/admin only takes http connections. 

However, in order to prevent XSS, it is imperative to check other inputs as well for javascript injections that the admin will execute when visiting the site inputted. Checks include sanitizing and encoding in order to make sure code is not executed.

Additionally, not including a vulnerable index or box would be an optimal remediation for this challenge.

