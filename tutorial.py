

import datetime, operator, random, string, math
import matplotlib.pyplot as plt

from random import randrange
from datetime import datetime, timedelta
from collections import defaultdict

END_TIME = datetime(year=2018, month=12, day=31)
START_TIME = datetime(year=2018, month=1, day=1)

def main():
    # get data that has text from users and times they were written
    data, user_names = generate_random_data()

    # bin data by user by month -- this is a nested dictionary comprehension -- it defines a dictionary by iterating over a range of month numbers and then defines it's values using another dictionary which has zero values for each user name
    posts_per_month = {datetime(year=2018, month=i, day=1).strftime('%B'): {un: 0 for un in user_names} for i in range(1, 13)}
    for post in data:
        posts_per_month[post['date'].strftime('%B')][post['user']] += 1
    # print(posts_per_month)

    # get the TOP_N most frequent words
    TOP_N = 20
    # nifty data structure that lets you not have to check if a key is already in there -- it uses a lambda function which is like defining a function on-the-fly which doesn't have a name -- this one simply returns zero -- it is called when you access a key that is not yet in the dictionary
    word_counts = defaultdict(lambda: 0)
    for post in data:
        words = post['text'].split(' ')
        for word in words:
            if word.strip() != '':
                word_counts[word] += 1
    # nifty sort function that returns tuples of (k,v) in decending order of values
    sort_wcs = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    # zip is a cool function that lets you split up and recombine tuples
    top_wn, top_wc = zip(*sort_wcs[:TOP_N])

    # subplot tells it to split your space into arg1 x arg2 plots and the third parameter tells it which cell in the grid to put things in -- all your subsequent plt calls will make things in this cell
    plt.subplot(2, 1, 1)
    # make plot of most frequent words
    plt.title('Distribution of Most Frequent Unigrams')
    plt.bar(range(TOP_N), top_wc)
    plt.xticks(range(TOP_N), top_wn, rotation=45)
    # tight layout helps make things not overlap
    plt.tight_layout()

    # tell matplotlib that your next calls will put things in the second cell (arg3 = 2)
    plt.subplot(2, 1, 2)
    # make plot of user activity over time
    plt.title('Number of User Posts Over Time')
    for user_name in user_names:
        # give it the range and the y-values along with marker-- which tells it to add the points to the line
        plt.plot(range(12), [posts_per_month[k][user_name] for k in posts_per_month], marker='o')
    plt.xticks(range(12), posts_per_month.keys(), rotation=45)
    plt.legend(user_names)
    plt.tight_layout()
    # grid looks nice sometimes -- it puts lines behind your plot which can make it easier to read
    plt.grid()

    # you can save or show or both -- if you show first it won't save correctly
    plt.savefig('test.png')
    plt.show()

# pretend you have some posts from some users
def generate_random_data():
    num_users = 3
    num_posts = 1000
    user_names = ['user_' + str(i+1) for i in range(num_users)]
    # split_points = [random.random() for i in range(num_users-1)]
    split_points = [1.0/num_users*(i+1) for i in range(num_users-1)]

    posts = []
    for i in range(num_posts):
        user_index = sum([1 for j in split_points if i*1.0/num_posts > j])
        post = {'user': user_names[user_index], 'text': make_words(), 'date': make_time()}
        posts.append(post)
    return posts, user_names

# make random dates for the posts
def make_time():
    delta = END_TIME - START_TIME
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return START_TIME + timedelta(seconds=random_second)

# make up words to generate posts
def make_words():
    # how long should the words be?
    str_len = 3
    # how long should the sentences be? in range 0-99
    sent_len = int(math.floor(100 * random.random()))
    sent = ' '.join([''.join(random.choices(string.ascii_uppercase, k=str_len)) for i in range(sent_len)])
    return sent

if __name__ == '__main__':
    main()
