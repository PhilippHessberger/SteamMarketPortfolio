Hi! This is a hobby project to keep track of my steam cs2 inventory's progress.

It basically just downloads your steam market transaction history while ignoring other games, writes them to a .csv file and then plots the content of said .csv file on a graph.

To use it, just replace your username and password in main.py and then watch your steam authenticator for a login try.

It takes a few seconds to login, because the program gives you 10 seconds to accept the login on the authenticator. It also takes some time to download the market history data because of the api call/second limit steamcommunity.com has. You can see the progress in the console output.

Disclaimer: I didn't write any intentionally malicious code, but I do not take responibility for anything you do with it or anything that happens to you.
