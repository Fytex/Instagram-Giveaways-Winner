from contextlib import contextmanager
from selenium import webdriver # type: ignore

class ImplicitlyWait:
    def __init__(self, driver:webdriver, timeout:int):
        self.driver = driver
        self.timeout = timeout

    def enable(self):

        '''

        Enable implicitly wait so it doesn't throw errors without waiting some time in order to let the element appear

        '''

        self.driver.implicitly_wait(self.timeout)

    def disable(self):

        '''

        Disable implicitly wait so it doesn't wait for the element to appear. This can cause errors if not handled with a 'Explicitly Wait'

        '''

        self.driver.implicitly_wait(0)

    @contextmanager
    def ignore(self):

        '''

        Ingore implicitly wait in the current block of code by disabling and enabling again when finished

        '''

        try:
            yield self.disable()
        finally:
            self.enable()
