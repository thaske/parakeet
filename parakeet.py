import praw, re, datetime

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('mechmarket')
item = 'HHKB'
low = 25
high = 300

for submission in subreddit.stream.submissions():

    # process titles to only include items that are being sold
    if '[H]' in submission.title:
        items = re.findall(r'\[H\](.*?)\[W\]', submission.title)
        items = "".join(items).replace('\n','').lstrip()
        # print(items)    # debugging purposes

    # shorten url
    url = f'reddit.com/{submission.id}'
    time = datetime.datetime.fromtimestamp(submission.created)

    # find posts containing the item
    if item in items:
        print('===============================')
        print(f'Found a submission!\nTitle: {submission.title}\nTime: {time}\nURL: {url}\n')

        prices = re.findall(r'\d+', submission.selftext)    # finds all numbers in the selftext
        print('Possible Price:')
        for price in prices:
            if int(price) > low and int(price) < high:        # general range for
                print(f'${price}')

        print('===============================\n\n')
