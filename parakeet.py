import praw, re, datetime

def main():
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit('mechmarket')

    item = 'Alps'
    low = 0
    high = 200

    for submission in subreddit.stream.submissions():
        process_submission(submission, item, low, high)

def process_submission(submission, item, low, high):

    # process titles to only include items that are being sold
    items = re.findall(r'\[H\](.*?)\[W\]', submission.title)
    items = "".join(items).replace('\n','').lstrip()

    # shorten url
    url = f'reddit.com/{submission.id}'
    time = datetime.datetime.fromtimestamp(submission.created)

    # find posts containing the item
    if item in items:
        print('===============================')
        print(f'Found a submission!\nTitle: {submission.title}\nTime: {time}\nURL: {url}\n')

        prices = re.findall(r'\d+(?<!%)', submission.selftext)    # finds all numbers in the selftext
        print('Possible Price:')
        for price in prices:
            if int(price) > low and int(price) < high:        # only display prices that would be reasonable for the item
                print(f'${price}')

        print('===============================\n\n')

if __name__ == '__main__':
    main()
