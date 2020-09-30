import os

from selenium import webdriver # type: ignore
from typing import Optional
from sys import platform

class Browser:
    def __init__(self, window:bool=True, binary_location:Optional[str]=None, default_lang:bool=False, **kwargs):

        if platform == 'linux' or platform == 'linux2':
            driver_file_name = 'chrome_linux'
        elif platform == 'win32':
            driver_file_name = 'chrome_windows.exe'
        elif platform == 'darwin':
            driver_file_name = 'chrome_mac'

        driver_path = os.path.join(os.getcwd() , f'drivers{os.path.sep}{driver_file_name}')

        os.chmod(driver_path , 0o755)

        options = webdriver.ChromeOptions()

        if not default_lang:
            options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        options.headless = not window ;

        if binary_location:
            options.binary_location = binary_location


        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)


class Tab:

    def __init__(self, driver:webdriver.Chrome, url:str):
        self.driver = driver
        self.url = url


    def new_tab(self, url:str='https://www.google.com'):

        '''

        Opens a new tab on Browser

        Args:
            - url : to navigate after openning tab

        '''

        self.driver.execute_script(f'window.open(\'{url}\');')
        self.driver.switch_to.window(self.driver.window_handles[-1])


    def close_tab(self):

        '''

        Close the last tab on Browser

        '''

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1]) # could write 'main' but later on could be modified


    def __enter__(self):
        self.new_tab(self.url)


    def __exit__(self, *exc):
        self.close_tab()
