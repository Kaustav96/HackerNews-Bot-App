import requests
import json
import pprint
from datetime import datetime
import time
import schedule
from slack_client import slacker
from slack_client import slacker_file
from tabulate import tabulate
import self as self
from bs4 import BeautifulSoup
import  logging


page_no = 1
FILE_NAME = 'hacker_news_data.json'

SHORT_HEADERS = ["Title", "Link", "Points"]
FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')

def save_json(x):
    with open(FILE_NAME, 'a') as f:
        json.dump(x, f)


def sort_stories_by_votes(hn):
    save_json(sorted(hn, key=lambda k:k['votes']))
    return sorted(hn, key=lambda k: k['votes'])


hn = []


def get_news_page(self, page_no):

    try:

        res = requests.get('https://news.ycombinator.com/news?p='+str(page_no))
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        if len(subtext) > 0:
            def create_custom_hackernews(links, subtext):

                for innx, item in enumerate(links):
                    title = links[innx].getText()  # getText() will help in getting the title of the link
                    href = links[innx].get('href', None)
                    vote = subtext[innx].select('.score')
                    if len(vote):
                        points = int(vote[0].getText().replace(' points', ''))
                        if points > 99:
                            hn.append({'title': title, 'link': href, 'votes': points})
                return sort_stories_by_votes(hn)
            (create_custom_hackernews(links, subtext))
            page_no = page_no + 1
            get_news_page(self, page_no)

        else:
            # print(len(hn))
            new_dict = {}
            for item in hn:
                title = item['title']
                new_dict[title] = item
                # print(new_dict[title]['title'])
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print('Sent news to the Slack App - ', dt_string)

            table = tabulate(new_dict.values(), tablefmt='grid')
            # print(table)

            FILE_TABLE_NAME = 'final_news_list.txt'
            with open(FILE_TABLE_NAME, 'w') as file:
                file.write(table)
            slacker_file()
            logging.warning('Attachment has been sent to slack')
            print('\n')
            # slack_text = f'Please find News From Hacker-News below:{table}'
            # slacker()(slack_text)

            # table = tabulate(hn)
            # print(table)

            return
    except Exception as e:
        slacker()(f'Exception occurred: [{e}]')
        logging.error(e)
        print(f'Exception Occurred :{e}')


schedule.every(10).minutes.do(self.self, get_news_page(self, page_no))
while True:
    # Checks whether a scheduled task
    # is pending to run or not
    # print("Current time ran job at - ",time.time())
    schedule.run_pending()
    time.sleep(1)
