from configparser import ConfigParser
from modules.instagram_bot import Bot
from functools import partial
from random import triangular
from re import search


ASCII = '''
\n\n
\t\t\t .----------------.  .----------------.  .----------------. 
\t\t\t| .--------------. || .--------------. || .--------------. |
\t\t\t| |  ____  ____  | || |   _    _     | || |    ______    | |
\t\t\t| | |_   ||   _| | || |  | |  | |    | || |   / ____ `.  | |
\t\t\t| |   | |__| |   | || |  | |__| |_   | || |   `'  __) |  | |
\t\t\t| |   |  __  |   | || |  |____   _|  | || |   _  |__ '.  | |
\t\t\t| |  _| |  | |_  | || |      _| |_   | || |  | \____) |  | |
\t\t\t| | |____||____| | || |     |_____|  | || |   \______.'  | |
\t\t\t| |              | || |              | || |              | |
\t\t\t| '--------------' || '--------------' || '--------------' |
\t\t\t '----------------'  '----------------'  '----------------' 
\n\n\n\t\t\t\t\t\t\t\t\tCreated by: Fytex\n\n\n
'''


parser = ConfigParser()
parser.read('config.ini', encoding='utf8')

post_link = parser.get('Required', 'Post Link', fallback=None)
expr = parser.get('Required', 'Expression')
username = parser.get('Required', 'Username')
password = parser.get('Required', 'Password')


window = parser.getboolean('Optional', 'Window', fallback=True)
user_target = parser.get('Optional', 'User Target', fallback=None)
from_followers = parser.getboolean('Optional', 'Followers', fallback=True)
limit = parser.getint('Optional', 'Limit', fallback=None)
timeout = parser.getint('Optional', 'Timeout', fallback=30)
save_only = parser.getboolean('Optional', 'Save Only', fallback=False)


low = parser.getint('Interval', 'Min', fallback=60)
high = parser.getint('Interval', 'Max', fallback=120)
mode = parser.getint('Interval', 'Weight', fallback=None) # None goes for midpoint


default_lang = parser.getboolean('Chrome', 'Default Lang', fallback=False)
binary_location = parser.get('Chrome', 'Location', fallback=None)


if not post_link and not save_only:
    exit('Post Link must be provided')

if save_only and not post_link and not user_target:
    exit('Must specify Post Link or User Target')


print(ASCII)

bot = Bot(window, timeout, binary_location, default_lang)

print('Logging in...')

bot.log_in(username, password)

print('Logged in successfully!')

connections = []

if limit and (save_only or search(r'(?<!\\)@', expr)):
    if not user_target:
        print('Searching for post\'s owner')
    
        user_target = bot.get_user_from_post(post_link)
    
        print('Post\'s owner found!')

    print(f'Searching and saving {"followers" if from_followers else "followings"}...')

    connections = bot.get_user_connections(user_target,
                                       limit=limit,
                                       followers=from_followers)

    print(('followers' if from_followers else 'followings') + '\' database complete!')

if not save_only:
    print('Let\'s win this giveaway together! Spamming...')

    get_interval = partial(triangular, low, high, mode)
    
    bot.comment_post(post_link, expr, connections, get_interval)

print('Program finished with success!')
