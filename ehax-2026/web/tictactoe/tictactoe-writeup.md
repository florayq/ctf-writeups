# EHAX CTF 2026: web/tictactoe

## Context & Vulnerability
This is a tictactoe game platform against the unbeatable 'AI' (probably just an algorithm) tictactoe bot. 

For those who might be experienced in playing tictactoe, you may notice that since the user goes first on the board, we should have the advantage and be able to win.

When inspecting the page, we can read through the javascript and find that the flag is sent from the server in JSON format given to data. If data.flag is not empty, then the flag will be printed out. The question is now how to trigger the server to dump the flag. 

The requests can be analyzed through Burpsuite. The data sent from the client can be modified in the proxy tab. The data is in the format '3x3' and then a matrix of 0s, 1s and -1s, to signify:
- 0 for empty box
- 1 for box taken by player
- -1 for box taken by bot

This means we are able to modify the data sent. I could totally change the matrix so that the user wins.

## Background Information: CSRF
### What is CSRF (Cross-site request forgery)?
CSRF is a web security vulnerability that allows attackers to modify user requests sent to the server, causing victims to send requests they didn't intend to. This can cause users to send change password requests, request sensitive data, or transfer funds to another account when they didn't intend to in the first place.

In our case, we can use Burpsuite to change our own requests. 

## Exploitation
First, since it is an unbeatable bot, we can try making a board where we will win. The server will respond with a message saying 'nice try'.

If winning is not the solution, perhaps changing the dimensions?
Rather than the '3x3' value in the data, we could increment and change it to '4x4'. The server returns a hint of dimensional shift.

Thus, we change the matrix to be 4x4 as well. The flag is returned. 

EH4X{D1M3NS1ONAL_GHOST_1N_TH3_SH3LL}

Note: when I solved the challenge, I also filled the 4x4 matrix with all 1s which I don't think is required for getting the flag.

## Remediation
Remediations for this could be encrypting the data, keeping track of what moves were made, and checking that the matrix and values are 3x3. This will eliminate people trying to cheat the game or have the server side malfunction. 

## Credits
https://portswigger.net/web-security/csrf
