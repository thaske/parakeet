from chump import Application
import praw, re, datetime

def main():
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('mechmarket')

    app = Application()     # app token
    user = app.get_user()   # user token

    item = 'HHKB'
    low = 100
    high = 250

    for submission in subreddit.stream.submissions():

         l = process_submission(submission, item, low, high)
         if l[0] == True:
             message = user.send_message(
                 title = l[1],
                 message =  l[2],
                 url = l[3],
                 html = True,
                 sound = None
             )


def process_submission(submission, item, low, high):

    # edit post title to only include items that are being sold
    items = re.findall(r'\[H\](.*?)\[W\]', submission.title)
    items = "".join(items).replace('\n','').lstrip()

    title = f'Found {item}'
    time = datetime.datetime.fromtimestamp(submission.created)
    msg = f'<div>{submission.title}</div><div>{time}</div>'
    url = f'reddit.com/{submission.id}'

    if item in items:
        return [True, title, msg, url]
    else:
        return [False]

    # find posts containing the item
    '''
    if item in items:

        # log to console
        print('===============================')
        print(f'Found a submission!\nTitle: {submission.title}\nTime: {time}\nURL: {url}\n')

        prices = re.findall(r'\d+(?<!%)', submission.selftext)    # finds all numbers in the selftext in order to guess price
        print('Possible Price:')
        for price in prices:
            if int(price) > low and int(price) < high:        # only display prices that would be reasonable
                print(f'${price}')

        print('===============================\n\n')

        # send notification
    '''

if __name__ == '__main__':
    main()
