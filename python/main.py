import sys

import requests as requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

podcast_url = sys.argv[1]
download_directory = sys.argv[2]
binary_directory = sys.argv[3]
podcast_list = []
print(sys.argv)

options = Options()
options.binary_location = binary_directory
options.set_preference("media.volume_scale", "0.0")
browser = webdriver.Firefox(options=options)
browser.get(podcast_url)


def get_play_links():
    """ This method gets all the links to the podcast."""
    play_list = browser.find_elements(By.CSS_SELECTOR, '.play')
    for play in play_list:
        anchor = play.find_element(By.TAG_NAME, 'a')
        podcast_list.append(anchor.get_attribute('data-href').replace('autoplay=true', 'autoplay=false'))


def use_pagination():
    """ This method allows you to navigate through pagination """
    pagination = browser.find_element(By.CSS_SELECTOR, '.pagination')
    pagination_links = pagination.find_elements(By.TAG_NAME, 'a')
    next_page = pagination_links[-1]
    next_page_link = next_page.get_attribute('href')

    if next_page_link.endswith('#'):
        return False

    browser.get(next_page_link)

    return True


def clean_text(input_text):
    output_text = input_text.replace('/', '-')
    output_text = output_text.replace(' ', '_')
    return output_text


def add_zeros(number):
    while len(number) < len(str(len(podcast_list))):
        number = "0" + number

    return number


def download_podcast(number):
    try:
        browser.get(podcast_link)
        title = browser.find_element(By.TAG_NAME, 'h1').text
        browser.find_elements(By.ID, 'lnk_download')[1].click()
        browser.find_element(By.ID, 'dlink').click()
        response = requests.get(browser.current_url, allow_redirects=True)
        open(download_directory + add_zeros(number) + '_' + clean_text(title) + '.mp3', mode='wb').write(
            response.content)
    except Exception:
        print('Trying to download ' + podcast_link + ' again')
        download_podcast(number)


get_play_links()

while use_pagination():
    get_play_links()

podcast_list.reverse()
print("There are " + str(len(podcast_list)) + " links")
i = 0

for podcast_link in podcast_list:
    download_podcast(str(i))
    i += 1

browser.close()
