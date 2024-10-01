# Codewars Leaderboard

Welcome to the *Codewars Leaderboard*, a python terminal app that gets a list of users that you provide and ranks them in a leaderboard in your terminal.

### Features:
- **Grouping of users to separate them and rang within the groups**
- **Scheduled repeats for dynamically changing leaderboards**
- **Change dispaly modes based on your needs**

### How to use:

*Codewars Leaderboard* comes with a variety of features to fulfill all of your leaderboard needs. Here's how to take full advantage of them:

- **Positional arguments**
  - *Codewars Leaderboard* supports both files and individual usernames. When inputting positional arguments, *Codewars Leaderbaord* will differentiate between files and users, prioritizing files over users in the case that a file that is the same name as a user is inputted
- **Force types**
  - Although the file/user interpreter is pretty smart, sometimes you have a file named the same as a user and want to avoid ambiguity or you want the app to throw an error if a file doesn't exist instead of interpreting it as a user. This is where the --user (-u) and --file (-f) flags come in. By putting the --user or --file flag in front of an argument, it will be interpreted as a user or file respectively, giving you more control.
- **Groups**
  - *Codewars Leaderboard* supports the grouping of users. This can be useful if you are running a competition between two groups, or want to rank groups against themselves. To create a group, use the --group (-g) flag followed by what you want to name your group, and then any users you want in that group. Just like ungrouped users, groups can tell the difference between users and files, although you cannot force types within groups. If one user is placed in more than one group, then they will only be displayed with the last group they were placed in, but they will be ranked against all groups they are in
- **Schedule**
  - Using the --time (-t) flag followed by a number, you can have the leaderboard update every *t* minutes, also turning the leaderboard into a live display. If you ommit the time flag, the app will run once and print the leaderboard to the terminal
- **Display** *Only works with the grouping functionality!!!*
  -  *Codewars Leaderboard* has two display modes, *overall* and *grouped*. *Overall* is the default, where all users will be ranked in one overall leaderboard, with their group, if they have one. *Grouped*, signified using the --display (-d) flag, still has an overall leaderboard, but it also has additional, smaller leaderboards by group. *Note: If you are using a lot of groups, each individual group leaderboard will have less space avalliable, leading to formatting issues.*
- **Surpress**
  - If you want a cleaner output, you can use the --surpress (-s) flag, which will cause any user-related errors (not related to any file-related issues like existance errors) to not be shown
