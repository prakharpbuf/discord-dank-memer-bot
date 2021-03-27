from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select
import random
import bisect
from dotenv import dotenv_values


config = dotenv_values(".env")


class weighted_tuple(object):
    """
    >>> p = WeightedTuple({'A': 2, 'B': 1, 'C': 3})
    >>> len(p)
    6
    >>> p[0], p[1], p[2], p[3], p[4], p[5]
    ('A', 'A', 'B', 'C', 'C', 'C')
    >>> p[-1], p[-2], p[-3], p[-4], p[-5], p[-6]
    ('C', 'C', 'C', 'B', 'A', 'A')
    >>> p[6]
    Traceback (most recent call last):
    ...
    IndexError
    >>> p[-7]
    Traceback (most recent call last):
    ...
    IndexError
    """

    def __init__(self, items):
        self.indexes = []
        self.items = []
        next_index = 0
        for key in sorted(items.keys()):
            val = items[key]
            self.indexes.append(next_index)
            self.items.append(key)
            next_index += val

        self.len = next_index

    def __getitem__(self, n):
        if n < 0:
            n = self.len + n
        if n < 0 or n >= self.len:
            raise IndexError

        idx = bisect.bisect_right(self.indexes, n)
        return self.items[idx-1]

    def __len__(self):
        return self.len


class discord_bot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome('./driver/chromedriver')
        self.rechecked = False
        self.pm_replied = True
        self.commands = weighted_tuple({'pls sell fish': 15, 'pls sell': 10, 'pls deposit': 30, 'pls beg': 50, 'pls fish': 30, 'pls pm': 30,'pls highlow': 40, '***__I am a bot, this is being performed automatically__***': 15, 'pls balance': 20, 'pls hunt': 30, 'pls search': 30})
        self.acceptable_places = ['air', 'van', 'sink', 'attic', 'vacuum','bed', 'tree', 'shoe', 'discord', 'grass', 'couch', 'coat', 'pantry']

    def close_browser(self):
        self.driver.close()

    def login(self):
        browser = self.driver
        browser.get("https://discordapp.com/login")
        time.sleep(5)
        email = browser.find_element_by_name('email')
        for char in self.email:
            email.send_keys(char)
            time.sleep(0.1)
        password = browser.find_element_by_name('password')
        for char in self.password:
            password.send_keys(char)
            time.sleep(0.1)
        login_button = browser.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
        login_button.click()
        time.sleep(10)

    def goto_server(self, server_from_top):
        browser = self.driver
        server = browser.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/nav/ul/div[2]/div[3]/div['+str(server_from_top)+']/div[2]')
        server.click()

    def get_chatbox(self):
        self.box = self.driver.find_element_by_xpath("/html/body/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/main/form/div/div/div/div/div/div[3]/div[2]/div")

    def get_command(self):
        self.cur_command = random.choice(self.commands)
        if(self.cur_command == "pls sell fish"):
            self.cur_command = self.cur_command + \
                ' ' + str(random.randint(1, 3))
        elif(self.cur_command == "pls deposit"):
            self.cur_command = self.cur_command + \
                ' ' + str(random.randint(500, 1000))

    def enter_command(self):
        self.get_chatbox()
        for char in self.cur_command:
            self.box.send_keys(char)
            time.sleep(0.1)
        self.box.send_keys(Keys.RETURN)
        time.sleep(3)
        if(self.cur_command == "pls pm"):
            self.pm_replied = False
            self.check_reply()

    def goto_channel(self, channel):
        browser = self.driver
        channel_number = int(channel) + 2
        channel_element = browser.find_element_by_xpath('//*[@id="channels"]/div/div[' + str(channel_number) + ']')
        channel_element.click()

    def check_reply(self):
        self.get_chatbox()
        browser = self.driver
        message_div_selector = '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2)'
        message_div = browser.find_element_by_css_selector(message_div_selector)
        if("background" in message_div.get_attribute("class")):
            message_div_selector = '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div'

        index = 1
        div_class = browser.find_element_by_css_selector(message_div_selector + '> div:nth-child(' + str(index) + ')')
        if("contents" not in div_class.get_attribute("class")):
            index = 2

        last_message_from = ''
        try:
            last_message_from = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > h2 > span > span').text
        except Exception:
            try:
                last_message_from = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > h2 > span > span').text
            except Exception:
                pass

        if last_message_from != "Dank Memer":
            if not self.rechecked:
                time.sleep(10)
                self.rechecked = True
                self.check_reply()
            else:
                self.rechecked = False
                return
        self.rechecked = False

        if 'pls fish' in self.cur_command:
            message = ''
            try:
                message = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > div').text
            except Exception:
                return
            if 'Type' in message or 'type' in message or 'typing' in message or 'Typing' in message:
                code = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > div > code').text
                if code != None:
                    # arr = code.split('&#65279;')
                    # to_type = ' '.join(arr)
                    to_type = code
                    self.box.send_keys(to_type)
                    self.box.send_keys(Keys.RETURN)
        
        if 'pls hunt' in self.cur_command:
            message = ''
            try:
                message = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div > div:nth-child(' + str(index) + ') > div').text
            except Exception:
                try:
                    message = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > div').text
                except Exception:
                    pass
            if 'Type' in message or 'type' in message or 'typing' in message or 'Typing' in message:
                try:
                    code = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div > div:nth-child(' + str(index) + ') > div > code').text
                except Exception:
                    try:
                        code = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(' + str(index) + ') > div > code').text
                    except Exception:
                        pass
                if code != None:
                    self.box.send_keys(code)
                    self.box.send_keys(Keys.RETURN)


        elif 'pls pm' in self.cur_command:
            text = ''
            try:
                text = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div > div:nth-child(2) > div').text
            except Exception:
                try:
                    text = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(2) > div').text
                except Exception:
                    if not self.pm_replied:
                        self.get_chatbox()
                        self.box.send_keys(random.choice(['i', 'k', 'c']))
                        self.box.send_keys(Keys.RETURN)
                        self.pm_replied = True
            if 'broken' in text:
                for char in 'pls withdraw 3000':
                    self.box.send_keys(char)
                    time.sleep(0.1)
                self.box.send_keys(Keys.RETURN)
                time.sleep(1)
                self.get_chatbox()
                for char in 'pls buy laptop':
                    self.box.send_keys(char)
                    time.sleep(0.1)
                self.box.send_keys(Keys.ENTER)

        elif 'pls highlow' in self.cur_command:
            text = '0'
            try:
                text = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(3) > div > div > div:nth-child(3) > strong').text
            except Exception:
                return
            if(int(text) > 50 and int(text) < 75):
                self.box.send_keys(random.choice(weighted_tuple({'high':1, 'low':2})))
            elif int(text) >= 75:
                self.box.send_keys('low')
            elif int(text) <=50 and int(text)>25:
                self.box.send_keys(random.choice(weighted_tuple({'high':2, 'low':1})))
            else:
                self.box.send_keys('high')
            self.box.send_keys(Keys.ENTER)

        elif 'pls search' in self.cur_command:
            places = []
            try:
                places = browser.find_elements_by_css_selector(
                    '#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2) > div:nth-child(1) > div > code')
            except Exception:
                pass
            for place in places:
                if place.text in self.acceptable_places:
                    self.box.send_keys(place.text)
                    self.box.send_keys(Keys.ENTER)
                    break


# To be implemented later, to check for random events created by dank memer
    # def check_event(self):
    #     browser = self.driver
    #     while(1):
    #         last_message = browser.find_element_by_css_selector('#app-mount > div.app-1q1i1E > div > div.layers-3iHuyZ.layers-3q14ss > div > div > div.base-3dtUhz > div.content-98HsJk > div.chat-3bRxxu > div.content-yTz4x3 > main > div > div > div > div > div:nth-last-child(2)')

if __name__ == "__main__":
    bot = discord_bot(config['username'], config['password'])
    bot.login()
    bot.goto_server(config['server'])
    time.sleep(0.5)
    bot.goto_channel(config['channel'])
    bot.get_chatbox()
    i = 0
    while(i < 500):
        i = i+1
        if i % 100 == 0:
            time.sleep(random.randint(400, 600))
        bot.get_command()
        bot.get_chatbox()
        bot.enter_command()
        time.sleep(1)
        bot.check_reply()
        time.sleep(random.randint(10, 15))
    bot.close_browser()



