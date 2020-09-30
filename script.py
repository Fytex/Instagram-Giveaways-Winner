import signal

from re import search
from typing import List
from modules import Bot, Tab
from random import triangular
from functools import partial
from configparser import ConfigParser



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


user_target = parser.get('Optional', 'User Target', fallback=None)
from_followers = parser.getboolean('Optional', 'Followers', fallback=True)
limit = parser.getint('Optional', 'Limit', fallback=None)
specific_file = parser.get('Optional', 'Specific File', fallback=None)
force_search = parser.getboolean('Optional', 'Force Search', fallback=False)
save_only = parser.getboolean('Optional', 'Save Only', fallback=False)


low = parser.getint('Interval', 'Min', fallback=60)
high = parser.getint('Interval', 'Max', fallback=120)
weight = parser.getint('Interval', 'Weight', fallback=None) # None goes for midpoint


window = parser.getboolean('Browser', 'Window', fallback=True)
default_lang = parser.getboolean('Browser', 'Default Lang', fallback=False)
binary_location = parser.get('Browser', 'Location', fallback=None)
timeout = parser.getint('Browser', 'Timeout', fallback=30)

if not post_link:
    if not save_only:
        exit('Post Link must be provided or enable Save Only')

    if save_only and not user_target:
        exit('Must specify Post Link or User Target')

if specific_file:

    if save_only:
        exit('Either choose a Specifc File or Save Only')

    if force_search:
        exit('Either choose a Speciic File or Force Search')

if limit:
    if force_search:
        exit('Force Search only works if limit is disabled. Otherwise it will always force search to the limit')


    does_mention = bool(search(r'(?<!\\)@', expr))

    if does_mention and limit <= 0:
        exit('Limit must be > 0')

if not save_only and not low <= weight <= high:
    exit('Weight must be a number between Min and Max')


print(ASCII)

CONNECTIONS_TYPE = "followers" if from_followers else "followings"

records_path = 'records//' + CONNECTIONS_TYPE

bot = Bot(window, binary_location, default_lang, timeout=timeout, records_path=records_path)


print('Logging in...')

bot.log_in(username, password)

print('Logged in successfully!')


connections : List[str] = []

if specific_file:
    bot.get_user_connections_from_records(specific_file=specific_file, limit=limit)

elif save_only or does_mention:

    success = False

    if not user_target:
        print('Searching for post\'s owner')

        user_target = bot.get_user_from_post(post_link) # type: ignore  # post_link is 'str' because it exits otherwise. However appears as 'Optional[str]'

        print('Post\'s owner found!')

    print(f'Searching for {user_target}\'s {CONNECTIONS_TYPE} in records')


    success = bot.get_user_connections_from_records(user_target, limit=limit, followers=from_followers)

    if not success or force_search:

        if limit:
            print(f'Got {len(bot.connections)}/{limit} {CONNECTIONS_TYPE}. Still not enough...')

        print(f'Searching for {user_target}\'s {CONNECTIONS_TYPE} on Instagram')


        count_connections_in_record = len(bot.connections)
        to_quit = False

        try:
            user_target_url = bot.url_base + user_target

            if save_only:

                bot.driver.get(user_target_url)
                bot.get_user_connections_from_web(limit, from_followers, force_search)

            else:

                with Tab(bot.driver, user_target_url):
                    bot.get_user_connections_from_web(limit, from_followers, force_search)

        except KeyboardInterrupt: # Handle this error in case SIGINT is raised ('ctrl + c')
            to_quit = True


        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.SIG_IGN) # Ignore SIGINT
        connections_added_count = len(bot.connections) - count_connections_in_record

        if connections_added_count:
            bot.save_connections(user_target, bot.connections[-connections_added_count:])

        if to_quit:
            bot.quit(f'Early termination. Added {connections_added_count} so far. Making it a total of {len(bot.connections)} {CONNECTIONS_TYPE} in records.')
        else:
            print(f'{connections_added_count} found on Instagram. Having a total of {len(bot.connections)} {CONNECTIONS_TYPE} in records.')
            signal.signal(signal.SIGINT, original_sigint) # Set Original SIGINT back

    else:
        print(f'{len(bot.connections)} {CONNECTIONS_TYPE} found in records! No need to search for them on Instagram.')



if not save_only:
    print('Let\'s win this giveaway together! Spamming...')

    get_interval = partial(triangular, low, high, weight)

    try:
        bot.comment_post(post_link, expr, get_interval) # type: ignore  # post_link is 'str' because it exits otherwise. However appears as 'Optional[str]'

    except: # Handle this error in case SIGINT is raised ('ctrl + c') [Can't use KeyboardInterrupt because SIGINT could lead to more errors]
        signal.signal(signal.SIGINT, signal.SIG_IGN) # Ignore SIGINT
        bot.quit(f'Early termination. Sent {bot.num_comments} comments so far!')

    else:
        print(f'All possible comments were sent. A total of {bot.num_comments} comments!')


bot.quit('Program finished with success!')
