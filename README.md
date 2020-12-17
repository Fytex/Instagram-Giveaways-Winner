# Instagram-Giveaways-Winner

![GitHub top language](https://img.shields.io/github/languages/top/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/fytex/Instagram-Giveaways-Winner?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/fytex/Instagram-Giveaways-Winner?style=for-the-badge)


##### Instagram Bot which when given a post url will spam mentions to increase the chances of winning


## How does this bot work?
It works as a browser simulator using selenium. **[Only tested on Windows]**

At the beginning there are four steps (It will save data in order to don't waste your time):

1. Log in
2. Find post's owner
3. Find followers/followings
4. Start spamming mentions in the post


### Pre-Setup Warning

Before installing you need to be aware that this folder contains binary files (.exe, .etc) inside `drivers`' folder from an old ChromeDriver's release for a wider compatibility.

But don't worry... if you feel unsafe you can download these files by yourself (just put there because there are people who can't do these by themselves).

1. Go to chrome://settings/help and find out which is your Chrome's version
2. Go to https://chromedriver.chromium.org/downloads and find the latest version which supports your Chrome's version.
3. Download the one for your O.S.
4. Pick the executable and put in `drivers`' folder.
5. Replace and rename the executable with one that was already inside `driver`'s folder depending on your O.S. (You can get rid of the ones that were already inside the folder)


### Setup

1. Install Google Chrome (Check Browser's category in `config.ini` if you want a different path) -> if you guys start complaining about this specific step I'll make some updates to have wider options 
2. Install Python 3.6+ (Don't forget to add in system variable `PATH` [You can tick the following checkbox `Add Python 3.X to PATH` while installing Python])
3. Open terminal, change directory to Instagram-Giveaways-Winner's folder and type: `pip install -r requirements.txt`
4. Edit `config.ini` (See next category)
5. In the same terminal type: `py script.py`

Warning: Avoid resizing or touching the Browser opened. You can minimize if you want or if you want to get rid of it just change Window at Browser's category to `False` in `config.ini`

These commands can change depending on your configuration. Such as python/py/python3... or pip/pip3...

If you need help add me on discord or join the server and ask me (links in my profile's bio) :)


### All settings/credentials can be changed in config.ini.

Browser's window can be invisible (in background) if Window's option is deactivated.

- **Login** requires both username/email and password.
	- A cookie's data will be saved to login automatically in order to prevent repetitve actions.

- **Find post's owner** will only occur if no User Target is specified in the file.
    - User Target is the user where the bot will search for followers/followings to mention.
    - The timeout is a way to prevent blocking while trying to log in by stopping the program.

- **Find followers/followings** is where the bot searches and saves all followers/followings. 
    - You can specify the limit of followers/followings (it will pick the lowest one between the limit and the number of followers/followings from the User Target).
    - First it will search if there are the limit number of followers/followings inside a file in a specific file in records (database)
	- If Force Search is disabled and there is no limit and a file was found then it uses that amount of followers/followings to mention.
	- If Force Search is enabled or there aren't enough followers/followers in the file or file doesn't exist it will search on Instagram (User Target's followers/followings) until it meets the limit. If no limit specified then searches for all of them.
	- In `config.ini` you can either choose to search for followers or followings. 
    - The timeout is a way to prevent blocking while searching for followers/followings in case it gets stuck.
	- If you raise SIGNINT by pressing 'ctrl + c' in your keyboard. It will stop searching and will immediately save all followers/followings found into a file in records.
	- If you have a custom/specific file which you want to use just set the relative path at 'Specific File' in `config.ini`.

- **Start spamming mentions in the post** is where all the fun begins. It starts spamming mentions in the post.
    - By enabling SaveOnly's option this step won't run. This option is used in case you only want to save the followers/followings and use them later.
    - You can edit the message and add as many mentions as you want (mentions will never be repeated).
		- Interval's category in `config.ini` file lets you choose how much time it waits before each comment. You have to find out by yourself the best interval that fits into your account. It has a min, max and weight so the number isn't always the same preventing Instagram finding out it is a bot. (The smaller the interval the higher the chance of having to wait to comment again because of Instagram's A.I.) (You have to play with these numbers until you find out the best interval range for you)
		- In case you have a char that doesn't belong to BMP (such as some emojis) it will appear a different message. But your message will still be sent. (Refresh when finished or open in another browser to check everything is fine) 
	- By pressing 'ctrl+c' it raises SIGINT in order to stop the execution of the program.
    
    
    
### How do the records (database) work?

There are two sections:
  - followers
  - followings
  
Depending on what you choose it will save in the respective directory. Then it will choose the file's name using the following format `{User Target}.txt` where `User Target` is the user where we got the followers/followings.
By following the same pattern you see on the other records (`@user` in each line) you can create a custom file (E.g. `custom.txt`) and enable Specific File in `config.ini` (removing `#`) and changing the value to the path (E.g. `records\custom.txt`)


### How do the cookies work (auto-login)?

When the program logs into your account it saves in a separated folder called `cookies` the correspondent cookie to use it in a next time. This prevents Instagram from blocking your account from suspicious activity because you logged in too many times.


### Warnings:

I would recommend using an alternative account which you aren't afraid of losing because it could go wrong in the worst case. However I've never experienced any bad situations using this script.

Instagram has a comment's request rate-limit to avoid spamming. From my research it has an algorithm which varies from user to user. Since Instagram doesn't provide a time for reset we have to try every x seconds. In `config.ini` at Interval's category you can choose the range of the intervale by setting the minimum, maximum and the most probable number for the interval between comments (Better a range of numbers instead of always the same number in order to avoid being rate-limited). If a message pops up saying that it couldn't post the comment its because you hit that rate-limit so you just have to wait. (You don't have to do anything its all automatic but if this happens you should consider raising those intervals)
If you want to be able to send more comments you have to make a good use of your account (following, commenting, liking, etc.). That's how Instagram's A.I.'s works.

#### Future Updates:
  - [ ] Add a followers/followings tracker so it won't repeat the count if we restart the bot
  - [ ] Find out the best interval between each comment for your account (This requires researching and planning by using a lot of my time. Don't see when this would release because I'm not being financially paid for this)
  - [ ] Compatibility with more browsers
  
  
### Known Bugs:
```py
	raise exception_class(message, screen, stacktrace)
		selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary
```	
  - Since Chrome has updated their files' location, you need to keep Chrome's Driver updated in sync with Google Chrome. In this case just go back to [Pre-Setup-Warning](https://github.com/Fytex/Instagram-Giveaways-Winner#pre-setup-warning) and follow the steps **or** alternately just check `config.ini`'s Browser's Category to fix it.
