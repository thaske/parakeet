from chump import Application
import praw, re, datetime, configparser

def main():
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('mechmarket')

    config = configparser.ConfigParser()
    config.read("pushover.ini")
    app = Application(config.get('Pushover', 'app_key'))     # app token
    user = app.get_user(config.get('Pushover', 'user_key'))   # user token

    item = 'HHKB'
    low = 0
    high = 250

    for submission in subreddit.stream.submissions():

         l = process_submission(submission, item, low, high)
         if l[0]:
             message = user.send_message(
                 title = l[1],
                 message =  l[2],
                 url = l[3],
                 url_title = 'Open Reddit',
                 html = True,
                 sound = 'cosmic'
             )


def process_submission(submission, item, low, high):

    # edit post title to only include items that are being sold
    items = re.findall(r'\[H\](.*?)\[W\]', submission.title)
    items = "".join(items).replace('\n','').lstrip()

    if item in items:
        title = f'Found {item}'

        prices = re.findall(r'\d+(?<!%)', submission.selftext) # finds all numbers in the selftext in order to guess price
        price_list = []
        for price in prices:
            if int(price) > low and int(price) < high:         # only display prices that would be reasonable
                price_list.append(price)
        price_list = list(map(str, price_list))                # convert prices to strings for easier manipulation
        price_list = ["$" + price for price in price_list]     # append $ to each price

        msg = f'<div>{items}</div>'
        for price in price_list:
            msg += f'<div>{price}</div>'
        url = f'reddit.com/{submission.id}'
        return [True, title, msg, url]

    else:
        return [False]

if __name__ == '__main__':
    main()
