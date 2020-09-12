# Instagram-Giveaways-Winner
Instagram Bot which when given a post url will spam mentions to increase the chances of winning


## How does this bot work?
It works as a browser simulator using selenium.

There are four steps:

1. Log in
2. Find user from post
3. Find followers/followings
4. Start spamming mentions in the post


### Setup

1. Install Python 3.6+
2. Open terminal, change directory to Instagram-Giveaways-Winner's folder and type: `pip install -r requirements.txt`
3. Edit config.ini (See next category)
3. In the same terminal type: `py script.py`

These commands can change depending on your configuration. Such as python/py/python3... or pip/pip3...


### All settings/credentials can be changed in config.ini.

Browser's window can be invisible (in background) if Window's option is deactivated.

- Step 1 requires both username/email and password.

- Step 2 will only occur if no UserTarget is specified in the file.
    - UserTarget is the user where the bot will get the followers/followings to mention.
    - The timeout is a way to prevent blocking while trying to log in by stopping the program.

- Step 3 is the search and find part where the bot saves all users.
    - You can specify the limit of users in the file (it will pick the lowest one between the limit and the number of followers/followings from the UserTarget, the higher the number is, more time will take).
    - In the file you can either choose followers or followings. 
    - The timeout is a way to prevent blocking while searching for followers/followings in case it gets stuck by stopping the program.

- Step 4 is where all the fun begins. It starts spamming mentions in the post.
    - By enabling SaveOnly's option this step won't run. This option is used in case you only want to save the followers/followings and use them later.
    - You can edit the message and add as many mentions as you want (mentions will never be repeated).
    
    
    
### How do the records (database) work?

There are two sections:
  - followers
  - followings
  
Depending on what you choose it will save in the respective directory. Then it will choose the file's name using the following format `{UserTarget}_{total}.json` where `UserTarget` is the user where we got the followers/followings and `total` is the number of users we got.
When searching for a `UserTarget` if the lowest one between the `limit` (in the config file)  and the number of followers/followings from the `UserTarget` is already met in a file then it will skip Step 2 and use that file automatically.

#### Future Updates:
  - [ ] Add a followers/followings tracker so it won't repeat the count if we restart the bot
  - [ ] Add a way to find followers/followings some at a time until it reaches the limit/maximum. This way we can find followers/followings and post comments in a cycle.
