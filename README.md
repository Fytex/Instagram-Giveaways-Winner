# Instagram-Giveaways-Winner

![GitHub top language](https://img.shields.io/github/languages/top/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/fytex/Instagram-Giveaways-Winner?style=for-the-badge)


##### Instagram Bot which when given a post url will spam mentions to increase the chances of winning


## How does this bot work?
It works as a browser simulator using selenium.

There are four steps:

1. Log in
2. Find user from post
3. Find followers/followings
4. Start spamming mentions in the post


### Pre-Setup Warning

Before installing you need to be aware that this folder contains binary files (.exe, .etc) inside `drivers`' folder from an old ChromeDriver's release for a wider compatibility.

But don't worry... if you feel unsafe you can install these files by yourself (just put there because there are people who can't do these by themselves).

1. Go to chrome://settings/help and find out which is your Chrome's version
2. Go to https://chromedriver.chromium.org/downloads and find the latest version which supports your Chrome's version.
3. Download the one for your O.S.
4. Pick the executable and put in `drivers`' folder.
5. Replace and rename the executable with one that was already inside `driver`'s folder depending on your O.S. (You can get rid of the ones that were already inside the folder)


### Setup

1. Install Google Chrome (Check `config.ini` Chrome's category if you want a different path) -> if you guys start complaining about this specific step I'll make some updates to have wider options 
2. Install Python 3.6+ (Don't forget to add in system variable `PATH`)
3. Open terminal, change directory to Instagram-Giveaways-Winner's folder and type: `pip install -r requirements.txt`
4. Edit config.ini (See next category)
5. In the same terminal type: `py script.py`

Warning: Avoid resizing or touching the Browser oppened. You can minimize if you want or if you want to get rid of it just change `Window` to `False` in `config.ini`

These commands can change depending on your configuration. Such as python/py/python3... or pip/pip3...

If you need help add me on discord or join the server and ask me (links in my profile's bio) :)


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
	- Interval Category in `config` file lets you choose how much time it waits before each comment. You have to find out by yourself the best interval that fits your account. It has a min, max and weight so the number isn't always the same preventing Instagram finding out it is a bot. (Later I will try to create kind of an A.I. to do this for you)
    
    
    
### How do the records (database) work?

There are two sections:
  - followers
  - followings
  
Depending on what you choose it will save in the respective directory. Then it will choose the file's name using the following format `{UserTarget}_{total}.json` where `UserTarget` is the user where we got the followers/followings and `total` is the number of users we got.
When searching for a `UserTarget` if the lowest one between the `limit` (in the config file)  and the number of followers/followings from the `UserTarget` is already met in a file then it will skip Step 2 and use that file automatically.



### How do the cookies work (auto-login)?

When the program logs into your account it saves in a separated folder called `cookies` the correspondent cookie to use it in a next time. This prevents Instagram from blocking your account from suspicious activity because you logged in too many times.


### Warnings:

I would recommend using an alternative account which you aren't afraid of losing because it could go wrong in the worst case. However I've never experienced any bad situations using this script.

Instagram has a comment's request rate-limit to avoid spamming. From my research it has an algorithm which varies from user to user. Since Instagram doesn't provide a time for reset we have to try every x seconds. We chose it to be every 10 seconds. If a message pops up saying that it couldn't post the comment its because you hit that rate-limit so you just have to wait. (You don't have to do anything its all automatic)


#### Future Updates:
  - [ ] Add a followers/followings tracker so it won't repeat the count if we restart the bot
  - [ ] Add a way to find followers/followings some at a time until it reaches the limit/maximum. This way we can find followers/followings and post comments in a cycle.
  - [ ] Add specific file from records (database) to use as users to mention
  - [ ] Find out the best interval between each comment for your account
  
  
### Known Bugs:
```py
	raise exception_class(message, screen, stacktrace)
		selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary
```	
  - Since Chrome has updated their files' location, Selenium hasn't fixed it yet. Check `config.ini` Chrome's Category to fix it.
