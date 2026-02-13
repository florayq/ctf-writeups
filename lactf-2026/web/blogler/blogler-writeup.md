# LA CTF 2026: web/blogler

## Context
Blogler is a blogging platform built in Flask where users register an account and write blog posts in Markdown. Users are also able to modify YAML configuration. 

The code has built-in checks for `../` and `/`(root) directory traversal in the YAML configuration. 

The **goal of the challenge** is to find the flag in a flag file on the server. 

## Vulnerability
By manipulating the username of the user, you are able to traverse different directories. 

## Exploitation
1. Notice the display_name function used to remove underscores and make usernames more readable or user friendly.

2. YAML supports anchors (&) and aliases (*), which creates references to the same object specified.


Using these points, we can craft a method to dump the flag file to the screen. 

1. Register any username and password

2. Alias and anchor `users` and a blog under `blogs` together.

3. For that specified blog, change the `name` to be a directory traversal that takes advantage of the display_name function's underscore removal. For example: `._._/._._/flag` or `_.._/_.._/flag`.

4. Update the config and click on `blogs`. 

## Remediation
This exploitation takes advantage of different features in the functionality of the program.

To prevent such exploitations, the programmer can add more validations against local file inclusion attacks, particularly after all modifications and before passing to a functionality. The programmer should also add input validation for the blog and registration (which they wrote `TODO` comments on). This will also prevent the directory traversals using custom usernames through the `/blogs` page. 


## Other

### Other things I noticed
1. In `app.run()`, debug is set to True. My initial thought process was to have that dump users if there may possibly be an admin user.

2. `/login` doesn't actually work. It gets redirected to a `/home` page that doesn't exist.

