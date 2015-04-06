from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException, ElementNotVisibleException
from time import sleep


def login(driver, email, password):
    # Get the login page
    driver.get("https://www.fanduel.com/p/login#login")
    elem = driver.find_element_by_id("email")
    elem.send_keys(email)
    elem = driver.find_element_by_id("password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)


def get_time_til_next(driver):
    # Get the login page
    driver.get("https://www.fanduel.com/p/Home")
    elem = driver.find_element_by_xpath("/html/body/section/div[2]/div[2]/div[1]/div/div[contains(concat(' ', normalize-space(@class), ' '), ' nextgame ')]/span[2]")
    time_til_next_game = elem.text
    return time_til_next_game


def make_picks(driver):
    url = "https://www.fanduel.com/e/Game/11108?tableId=8120927"
    url = "https://www.fanduel.com/e/Game/NBA_Salary_Cap_11198/view?tableId=8557389&tableHash=63dd19de0f2a970c183cfb152cc32e6b"
    driver.get(url)
    player_xpath = "/html/body/section/div[2]/div[4]/div[1]/section[1]/div[4]/table/tbody/tr"
    player_rows = driver.find_elements_by_xpath(player_xpath)
    for player_row in player_rows:
        # Check if we are over salary cap
        salary_left = "/html/body/section/div[2]/div[4]/div[1]/section[2]/header/div[2]/div[1]/span"
        try:
            salary = driver.find_element_by_xpath(salary_left)
            if '-' in salary.text:
                remove_player(driver)
            else:
                player_paths = driver.find_elements_by_xpath("/html/body/section/div[2]/div[4]/div/section[2]/section/ul/li/div[4]")
                salaries = [str(x.text) for x in player_paths]
                if '' not in salaries:
                    submit(driver)
                    return

            # Clear any possible alert if there is one
            alert = driver.switch_to_alert()
            alert_text = alert.text
            alert.accept()

        except NoAlertPresentException:
            pass
        except NoSuchElementException:
            pass

        position = player_row.find_element_by_class_name('player-position').text
        name = player_row.find_element_by_class_name('player-name').text
        fppg = player_row.find_element_by_class_name('player-fppg').text
        played = player_row.find_element_by_class_name('player-played').text
        fixture = player_row.find_element_by_class_name('player-fixture').text
        salary = player_row.find_element_by_class_name('player-salary').text
        print position, name, fppg, played, fixture, salary

        # Do not consider questionable
        try:
            player_row.find_element_by_class_name('player-badge-injured-possible')
            continue
        except NoSuchElementException:
            pass

        # Do not consider out
        try:
            player_row.find_element_by_class_name('player-badge-injured-out')
            continue
        except NoSuchElementException:
            pass

        try:
            add_player = player_row.find_element_by_class_name('player-add-button')
            add_player.click()

            # Clear any possible alert if there is one
            alert = driver.switch_to_alert()
            alert_text = alert.text
            alert.accept()

        except NoAlertPresentException:
            pass

    submit(driver)


def submit(driver):
    submit_xpath = "/html/body/section/div[2]/div[4]/div/section[2]/footer/div[2]/input"
    submit = driver.find_element_by_id("enterButton")
    submit.click()

    try:
        # Clear any possible alert if there is one
        alert = driver.switch_to_alert()
        alert.accept()

    except NoAlertPresentException:
        # This is successful submission
        return



def remove_player(driver):
    xpath = "/html/body/section/div[2]/div[4]/div[1]/section[2]/section[contains(concat(' ',     normalize-space(@class), ' '), ' roster ')]/ul/li/a/i"
    my_team = driver.find_elements_by_xpath(xpath)
    my_team = list(my_team)
    player_to_remove = choice(my_team)
    try:
        player_to_remove.click()
    except ElementNotVisibleException:
        print 'Failed remove'
        remove_player(driver)



if __name__ == '__main__':
    driver = webdriver.Firefox()
    login(driver, 'fakeaccount4@gmail.com', 'fakeaccount4')
    #get_time_til_next(driver)
    make_picks(driver)
    sleep(3)
    driver.close()
