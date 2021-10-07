import os
import smtplib
import ssl
import time
import logging
from email.mime.text import MIMEText

from selenium import webdriver


URL = os.getenv('URL')
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
DELAY = 60 * 30  # 30 minutes
SENDER_EMAIL = 'botpatroller@gmail.com'
PASSWORD = os.getenv('PASSWORD')
RECIPIENT_EMAILS = ['joeyzhou7002@gmail.com', 'karenehk@gmail.com', 'angelina.mow@gmail.com']
HTML_TEMPLATE = """<p>Hello,</p>


<p>I have detected changes in the following website <a href='{0}'>{0}</a>.</p>

<p>Before:</p>
{1}

<p>After:</p>
{2}


<p> Yours truly,</p>


<p>Patroller Bot, Joey's dedicated slave</p>"""


def run():
    logging.basicConfig(filename='debug.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug(f'Initializing bot with parameters url={URL}, delay={DELAY} seconds')

    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    if 'content.txt' in os.listdir():
        with open('content.txt', 'r') as f:
            prev_content = f.read()
    else:
        driver.get(URL)
        prev_content = driver.find_elements_by_class_name('entry-content')[0].text

    while True:
        driver.get(URL)
        content = driver.find_elements_by_class_name('entry-content')[0].text
        if prev_content != content:
            logging.info(f'Contents changed:\n{prev_content} \n\n to \n\n {content}')
            mail = MIMEText(HTML_TEMPLATE.format(URL, prev_content.replace('\n', '<br>'), content.replace('\n', '<br>')), 'html')
            mail['Subject'] = 'Vanier Website Changes Detected'
            mail_str = mail.as_string()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context())
            server.login(SENDER_EMAIL, PASSWORD)
            for email in RECIPIENT_EMAILS:
                server.sendmail(SENDER_EMAIL, email, mail_str)
            prev_content = content
            with open('content.txt', 'w') as f:
                f.write(content)
        else:
            logging.debug(f'No changes detected')

        time.sleep(DELAY)


if __name__ == '__main__':
    run()
