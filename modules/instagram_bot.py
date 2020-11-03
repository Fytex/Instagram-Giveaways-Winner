import re
import json

from pathlib import Path
from itertools import islice
from time import perf_counter, sleep
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from typing import List, Iterator, Callable, Optional
from selenium.webdriver.support.wait import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import WebDriverException, NoSuchElementException # type: ignore

from .browser import Browser
from .comments import Comments
from .implicitly_wait import ImplicitlyWait


class Bot(Browser):

    __version__ = '2.0.3'


    def __init__(self, *args, **kwargs):

        self.url_base = 'https://www.instagram.com/'
        self.url_login = self.url_base + 'accounts/login'
        self.timeout = kwargs.get('timeout', 30)
        self.records_path = kwargs['records_path']
        self.connections = []
        self.num_comments = 0 # Have to save in the instance in order to display in terminal in case user raises KeyboardInterrupt

        super().__init__(*args, **kwargs)

        self.implicitly_wait = ImplicitlyWait(self.driver, self.timeout)
        self.implicitly_wait.enable()


    def log_in(self, username:str, password:str):

        '''

        Logs into Instagram account using the given credentials

        Args:
            - username : user's username
            - password : user's password

        '''

        COOKIE_NAME = 'sessionid'

        self.driver.get(self.url_login)

        # Wait until Instagram's home page is visible
        WebDriverWait(self.driver, self.timeout).until(
                lambda x: 'js-focus-visible' in x.find_element_by_tag_name('html').get_attribute('class'))

        try:
            
            with self.implicitly_wait.ignore():
                self.driver.find_element_by_css_selector('div[role=dialog] button').click()
            
        except NoSuchElementException: # Popup doesn't appear to some people
            pass

        try:

            with open(f'cookies/{username}.json', 'r') as file:
                cookie = json.load(file)

        except FileNotFoundError:
            pass

        else:

            self.driver.add_cookie(cookie)

            # I find out that chrome sends a warning message after loading a cookie
            WebDriverWait(self.driver, self.timeout).until(
                lambda driver: driver.get_log('browser'))

            self.driver.refresh()


        if 'not-logged-in' in self.driver.find_element_by_tag_name('html').get_attribute('class'):

            username_input, password_input, *_ = self.driver.find_elements_by_css_selector('form input')

            username_input.send_keys(username)
            password_input.send_keys(password + Keys.ENTER)

            WebDriverWait(self.driver, self.timeout).until(
                lambda x: 'js logged-in' in x.find_element_by_tag_name('html').get_attribute('class'))

            cookie = self.driver.get_cookie(COOKIE_NAME)

            Path('cookies/').mkdir(exist_ok=True)

            with open(f'cookies/{username}.json', 'w') as file:
                json.dump(cookie, file)

    def get_user_connections_from_records(self, username:Optional[str]=None, specific_file:Optional[str]=None, limit:Optional[int]=None, followers:bool=True) -> bool:

        '''

        Connections means followers or followings depending on the chosen data

        Args:
            - username      : target's username
            - specific_file : file to open instead of searching for a {username}.txt
            - limit         : limit number of connections (followers/followings) to save
            - followers     : if True returns a list of user's followers, if False returns of user's followings

        Returns:
            - success: True if we could get the number of connections as the limit

        '''

        try:

            with open(specific_file or f'{self.records_path}//{username}.txt', 'r') as file:

                self.connections = list(map(lambda x: x.rstrip('\n'), islice(file, limit) if limit \
                                                                        else file.readlines()))

        except FileNotFoundError:
            pass

        else:

            if self.connections and not limit or len(self.connections) == limit:
                return True

        return False


    def save_connections(self, username:str, connections_ext:List[str]):

        '''

        Saves connections_ext in a file called {username}.txt

        Args:
            - username        : target's username
            - connections_ext : list of connections to be appended to the file

        '''

        Path(self.records_path).mkdir(parents=True, exist_ok=True)

        with open(f'{self.records_path}//{username}.txt', 'a') as file:
            file.writelines(line + '\n' for line in connections_ext)


    def get_user_connections_from_web(self, limit:Optional[int]=None, followers:bool=True, force_search:bool=False):

        '''

        Searches for connections from a specific user on the web
        (Connections means followers or followings depending on the chosen option)

        Args:
            - limit        : limit number of connections (followers/followings) to save
            - followers    : if True returns a list of user's followers, if False returns of user's followings
            - force_search : force searching connections

        '''

        connections_link = self.driver.find_element_by_css_selector('ul li a span' if followers \
            else 'ul li:nth-child(3) a span')


        try:
            connections_limit = connections_link.get_attribute('title') if followers else connections_link.text

            connections_limit = int(connections_limit.replace(',', '').replace('.', '').replace(' ', ''))

        except ValueError: # This might only happen on followings
            exit('''
                    You must choose a UserTarget which following < 10,000 users
                    This happens because instagram doesn't provide by source the whole number,
                    and it would be a pain to translate every possible letter
                ''')

        # There is no need to search for connections if the records have more or no limit is specified
        #  or user has less connections than records (otherwiser enable option -> Force Search)
        if not force_search and self.connections and (not limit or connections_limit < limit):
            return

        connections_link.click()

        WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role=dialog] > div > div:nth-of-type(2)')))

        self.driver.execute_script('''
            elem = document.querySelector('div[role=dialog] > div > div:nth-of-type(2)');
        ''')

        # Have to click once in order to load connections
        self.driver.find_element_by_css_selector('div[role=dialog] li > div > div:nth-of-type(2) > div:nth-of-type(2)').click()

        timestamp = perf_counter()

        limit = min(limit, connections_limit) if limit else connections_limit

        connections_set = set(self.connections) # Cloned connections as a 'set' for search O(1)
        # only need to search for a few more connections
        limit -= len(self.connections) # type: ignore  # limit appears to be 'Optional[int]' but in reality it is 'int' because of limit being defined as 'None' or 'int' as an argument
        connections_added_count = 0
        total_connections_searched = 0

        while perf_counter() - timestamp < self.timeout: # Timer to prevent being in a loop if semone unfollows while searching

            connections_list = self.driver.find_elements_by_css_selector('div[role=dialog] ul li span a')
            diff_connections_count = len(connections_list) - total_connections_searched

            if diff_connections_count > 0:

                total_connections_searched += diff_connections_count
                timestamp = perf_counter()
                count = 0

                for connection in connections_list[-diff_connections_count:]:

                    connection_username = '@' + connection.text

                    if connection_username not in connections_set:

                        self.connections.append(connection_username)

                        connections_added_count += 1

                        if not force_search and connections_added_count == limit:
                            return

                if total_connections_searched >= connections_limit: # This might only trigger when force_search is enabled
                    break


            self.driver.execute_script('''
                    elem.scrollTo(0, elem.scrollHeight);
                ''')


    def get_user_from_post(self, url:str) -> str:

        '''

        Find the owner of the url's post

        Args:
            - url : post's link

        '''

        self.driver.get(url)

        user = self.driver.find_element_by_css_selector('article[role=\'presentation\'] a') \
                                .get_attribute('href').split('/')[-2]
        return user


    def write_comment(self, comment:str):

        '''

        Writes a comment in Instagram's comment box

        Args:
            - comment : text to write

        '''

        # Click Comment's Box
        self.driver \
            .find_element_by_css_selector('article[role=\'presentation\'] form > textarea') \
            .click()

        # Write in Comment's Box
        comment_box = self.driver \
                        .find_element_by_css_selector('article[role=\'presentation\'] form > textarea') \
                        .send_keys(comment)

    def override_post_requests_js(self, comment:str):

        '''

            This method was created because ChromeDriver doesn't support characters outside of BMP.
            Executed javascript code in Chrome's Browser to be able to post those emojis and characters

            Explanation: It overrides HTTP POST requests method in order to change the body (in this case the comment)

            Args:
                comment: text to write
        '''


        self.driver.execute_script('''
            XMLHttpRequest.prototype.realSend = XMLHttpRequest.prototype.send;
            let re = RegExp('comment_text=.*&replied_to_comment_id=');

            var newSend = function(vData) {
                if (re.test(vData)) {
                    vData = 'comment_text=''' + comment + '''&replied_to_comment_id=';
                }

                this.realSend(vData);
            };
            XMLHttpRequest.prototype.send = newSend;
        ''')


    def send_comment(self) -> bool:

        '''

        Press 'Post' button in comment's box to send it

        '''

        try:

            # Click Post's Button to send Comment
            self.driver \
                .find_element_by_css_selector('article[role=\'presentation\'] form > button') \
                .click()

        except WebDriverException:
            sleep(60) # Couldn't comment error pop up. No specific css selector. (<p> was too risky because of pop up's warnings such as cookies one)

        with self.implicitly_wait.ignore(): # remove Implicit Wait since we are going to check for possible non-existent element and we don't want any cooldown

            # Wait the loading icon disappear
            WebDriverWait(self.driver, self.timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article[role=\'presentation\'] form > div')))

        # Text in Comment's Box
        return not self.driver.find_element_by_css_selector('article[role=\'presentation\'] form > textarea').text



    def comment_post(self, url:str, expr:str, get_interval:Callable[[], float]):

        '''

        Generates the comments from an expression and a list of connections then writes and finally sends

        Args:
            - url          : post's url to comment
            - expr         : expression representing comments' pattern
            - get_interval : generator which yields a waiting time

        '''


        expr_parts = re.split(r'(?<!\\)@', expr)
        n = len(expr_parts) - 1

        if self.driver.current_url != url:
            self.driver.get(url)

        def chunks() -> Iterator[str]:
            for idx in range(0, (len(self.connections) // n) * n, n):
                yield self.connections[idx:idx + n]

        comments = Comments(chunks(), expr_parts)


        for comment in comments.generate():
            success = False
            has_input = False

            while not success:

                if not has_input:
                    try:
                        self.write_comment(comment)

                    except WebDriverException: # This would be pretty sure a char/emoji not in BMP because ChormeDriver doesn't support.
                            self.override_post_requests_js(comment)
                            comment = '''
                                    Info: Message is fine. If you open this post in another browser you can see it is working. Can\'t show here the real message because there are some characters not supported by ChromeDriver (non-BMP chars)
                                    '''
                            self.write_comment(comment)

                    has_input = True


                success = self.send_comment()

                if success:
                    self.num_comments += 1

                sleep(get_interval())


    def quit(self, message:str=None):

        '''

        Close driver and quit program

        Args:
            - message : quitting program's text

        '''

        self.driver.quit()
        exit(message)
