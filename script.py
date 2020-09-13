from configparser import ConfigParser
from modules.instagram_bot import Bot


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

post_link = parser.get('Required', 'Post Link')
expr = parser.get('Required', 'Expression')
username = parser.get('Required', 'UserName')
password = parser.get('Required', 'Password')


window = parser.getboolean('Optional', 'Window', fallback=True)
user_connections = parser.get('Optional', 'UserTarget', fallback=None)
from_followers = parser.getboolean('Optional', 'Followers', fallback=True)
limit = parser.getint('Optional', 'Limit', fallback=None)
timeout = parser.getint('Optional', 'Timeout', fallback=30)
save_only = parser.getboolean('Optional', 'SaveOnly', fallback=False)

print(ASCII)

bot = Bot(window, timeout)

print('Logging in...')

bot.log_in(username, password)

print('Logged in successfully!')

if not user_connections:
    print('Searching for post\'s owner')
    
    user_connections = bot.get_user_from_post(post_link)
    
    print('Post\'s owner found!')

print(f'Searching and saving {"followers" if from_followers else "followings"}...')

connections = bot.get_user_connections(user_connections,
                                       limit=limit,
                                       followers=from_followers)

print(('followers' if from_followers else 'followings') + '\' database complete!')

if not save_only:
    print('Let\'s win this giveaway together! Spamming...')
    
    bot.comment_post(post_link, expr, connections)

print('Program finished with success!')
