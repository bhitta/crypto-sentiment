import csv
import os
from datetime import datetime
import pandas as pd
from selenium.common import exceptions
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

def create_chromium_instance():
    options = ChromeOptions()
    options.use_chromium = True
    #options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    return driver

def create_firefox_instance():
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = Firefox(options=options)
    return driver

def login_to_twitter(username, password, driver):
    url = 'https://twitter.com/login'
    try:
        driver.get(url)
        xpath_username = '//input[@name="text"]'
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_username)))
        uid_input = driver.find_element(By.XPATH, xpath_username)
        uid_input.send_keys(username)
    except exceptions.TimeoutException:
        print("Timeout while waiting for Login screen")
        return False

    try:
        uid_input.send_keys(Keys.RETURN)
        url = "https://twitter.com/i/flow/login"
        WebDriverWait(driver, 10).until(expected_conditions.url_to_be(url))

    except exceptions.TimeoutException:
        print("Timeout while waiting for home screen")

    try:
        xpath_password = '//input[@name="password"]'
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_password)))
        pwd_input = driver.find_element(By.XPATH, xpath_password)
        pwd_input.send_keys(password)
    except exceptions.TimeoutException:
        print("Timeout while waiting for Login screen")
        return False

    try:
        pwd_input.send_keys(Keys.RETURN)
        url = "https://twitter.com/home"
        WebDriverWait(driver, 10).until(expected_conditions.url_to_be(url))

    except exceptions.TimeoutException:
        print("Timeout while waiting for home screen")
    return True

def find_search_input_and_enter_criteria(search_term, driver):
    try:
        xpath_search = '//input[@aria-label="Search query"]'
        search_input = driver.find_element(By.XPATH, xpath_search)
        WebDriverWait(driver, 10)
    except exceptions.TimeoutException:
        print("Timeout while trying to find search input field")
        return False

    try:
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)
    except exceptions.TimeoutException:
        print("Timeout while trying to send search query")
        return False
    return True


def change_page_sort(tab_name, driver):
    """Options for this program are `Latest` and `Top`"""
    tab = driver.find_element(By.LINK_TEXT, tab_name)
    tab.click()
    xpath_tab_state = f'//a[contains(text(),\"{tab_name}\") and @aria-selected=\"true\"]'


def generate_tweet_id(tweet):
    return ''.join(tweet)


def scroll_down_page(driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
    """The function will try to scroll down the page and will check the current
    and last positions as an indicator. If the current and last positions are the same after `max_attempts`
    the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
    flag will be returned as `True`"""
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region

def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['User', 'Handle', 'PostDate', 'TweetText', 'Emojis', 'ReplyCount', 'RetweetCount', 'LikeCount']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)

def collect_all_tweets_from_current_view(driver, lookback_limit=25):
    """The page is continously loaded, so as you scroll down the number of tweets returned by this function will
     continue to grow. To limit the risk of 're-processing' the same tweet over and over again, you can set the
     `lookback_limit` to only process the last `x` number of tweets extracted from the page in each iteration.
     You may need to play around with this number to get something that works for you. I've set the default
     based on my computer settings and internet speed, etc..."""
    page_cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]/div[1]/div[1]/div[1]/div[2]/div[2]')
    if len(page_cards) <= lookback_limit:
        return page_cards
    else:
        return page_cards[-lookback_limit:]

def extract_data_from_current_tweet_card(card):
    try:
        user = card.find_element(By.XPATH, './/span').text
    except exceptions.NoSuchElementException:
        user = ""
    except exceptions.StaleElementReferenceException:
        return
    try:
        handle = card.find_element(By.XPATH, './/span[contains(text(), "@")]').text
    except exceptions.NoSuchElementException:
        handle = ""
    try:
        """
        If there is no post date here, there it is usually sponsored content, or some
        other form of content where post dates do not apply. You can set a default value
        for the postdate on Exception if you which to keep this record. By default I am
        excluding these.
        """
        postdate = card.find_element(By.XPATH, './/time').get_attribute('datetime')
    except exceptions.NoSuchElementException:
        return
    try:
        spans = card.find_elements(By.XPATH, './div[2]//span')
        _full_comment = ' '.join([element.text for element in spans])
    except exceptions.NoSuchElementException:
        _full_comment = ""
    try:
        emojis = card.find_elements(By.XPATH, './/img')
        all_emojis = ','.join([emoji.get_attribute('title') for emoji in emojis])
    except exceptions.NoSuchElementException:
        all_emojis = ""
    try:
        _responding = card.find_element(By.XPATH, './/div[2]/div[2]/div[2]').text
    except exceptions.NoSuchElementException:
        _responding = ""
    tweet_text = _full_comment #+ _responding
    try:
        reply_count = card.find_element(By.XPATH, './/div[@data-testid="reply"]').text
    except exceptions.NoSuchElementException:
        reply_count = ""
    try:
        retweet_count = card.find_element(By.XPATH, './/div[@data-testid="retweet"]').text
    except exceptions.NoSuchElementException:
        retweet_count = ""
    try:
        like_count = card.find_element(By.XPATH, './/div[@data-testid="like"]').text
    except exceptions.NoSuchElementException:
        like_count = ""
    tweet = (user, handle, postdate, tweet_text, all_emojis, reply_count, retweet_count, like_count)
    return tweet

def delete_cache(driver):
    driver.execute_script("window.open('');")
    sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    sleep(2)
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB * 7 + Keys.ENTER) # send right combination
    actions.perform()
    sleep(2)
    driver.close() # close this tab
    driver.switch_to.window(driver.window_handles[0]) # switch back

def main(username, password, search_term, filepath, page_sort='Latest', timestamp="temp02927"):
    save_tweet_data_to_csv(None, filepath, 'w')  # create file for saving records
    last_position        = None
    end_of_scroll_region = False
    timestamp_reached    = False
    unique_tweets        = set()

    driver = create_firefox_instance()
    logged_in = login_to_twitter(username, password, driver)
    if not logged_in:
        return

    search_found = find_search_input_and_enter_criteria(search_term, driver)
    if not search_found:
        return
    sleep(2) # firefox is slow
    change_page_sort(page_sort, driver)
    sleep(2) # make webdirver wait on the tweets to load
    scroll_count = 0
    while not end_of_scroll_region or timestamp_reached:
        cards = collect_all_tweets_from_current_view(driver)
        for card in cards:
            try:
                tweet = extract_data_from_current_tweet_card(card)
                try:
                    if tweet[2] == timestamp:
                        timestamp_reached = True
                        break
                except:
                    continue
#               try:
#                   print(tweet[2])
#               except:
#                   continue
            except exceptions.StaleElementReferenceException:
                continue
            if not tweet:
                continue
            tweet_id = generate_tweet_id(tweet)
            if tweet_id not in unique_tweets:
                unique_tweets.add(tweet_id)
                save_tweet_data_to_csv(tweet, filepath)
            if tweet[2] == timestamp:
                break
        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)
        #print("Scrolling ...")
        scroll_count =+ 1
        if scroll_count % 50 == 0:
            delete_cache(driver)
    print("End of scroll region reached.")
    driver.quit()

if __name__ == '__main__':
    usr = "sedimentalist"
    pwd = "sediment"
    ticker_tag  = "AVAX"
    month       = "11"
    year        = "2021"

    for day in reversed(range(1,19)):
        direction = "until"
        term = f'${ticker_tag} {direction}:{year}-{month}-{day}'
        print(term)
        path = f'./data/twitter/raw/{term}-raw.csv'
        #if os.path.exists(path):
        #    path = path[:-4] + "-" + str(datetime.now()) + path[-4:]

        # scrape from midnight of the day into the past
        main(usr, pwd, term, path)
       #timestamp = pd.read_csv(path).iloc[-1:]["PostDate"].tolist()[0]
       #print(timestamp)
       #direction = "since"
       #term = f'${ticker_tag} {direction}:{year}-{month}-{day}'
       #print(term)
       #path = f'./data/twitter/raw/{term}-raw.csv'
       ## scrape from beginning of day until timestamp of reverse crawler or scroll limit is met.
       #main(usr, pwd, term, path, timestamp=timestamp)