import time
import logging

from selenium import webdriver


URL = 'https://www.vaniercollege.qc.ca/sports-recreation/weekly-schedule/'
CHROME_DRIVER_PATH = 'C:\\Users\\zhouwuyue\\Documents\\patroller\\chromedriver.exe'
DELAY = 60


def run():
    logging.basicConfig(filename='debug.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug(f'Initializing bot with parameters url={URL}, delay={DELAY}')

    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    driver.get(URL)
    prev_content = driver.find_elements_by_class_name('entry-content')[0].text

    logging.debug('Fetched data, entering loop')
    while True:
        time.sleep(DELAY)
        driver.get(URL)
        content = driver.find_elements_by_class_name('entry-content')[0].text
        if prev_content != content:
            logging.info(f'Contents changed:\n{prev_content} \n\n to \n\n {content}')
            prev_content = content
        else:
            logging.debug(f'No changes detected')


if __name__ == '__main__':
    run()
