import re
import praw
import time
import pattern.en

fewer_response = "fewer %s*"

split_regex = re.compile(r"\w+|[^\w\s]")


def is_plural_noun(word):
    assert ' ' not in word
    return pattern.en.tag(word)[0][1] == 'NNS'


# given a string, return all words that ungrammatically follow 'less'
def get_mistakes(text):
    for line in text.splitlines():
        if line.startswith('>'):
            continue
        split = re.findall(split_regex, line)
        indices = [i for i, x in enumerate(split) if x.lower() == "less"]
        for index in indices:
            # skip if less is the last word
            if index == len(split) - 1:
                continue
            # don't correct 'more or less'
            if ' '.join(split[index - 2:index + 1]).lower() == 'more or less':
                continue

            # the word coming after less
            follower = split[index + 1]

            if is_plural_noun(follower):
                yield follower


def process_comment(com):
    if 'less' in com.body.lower():
        mistakes = set(get_mistakes(com.body))
        if mistakes:
            print(com.body)
            com.reply(
                '\n\n'.join((fewer_response.upper() if word.isupper() else fewer_response) % word for word in mistakes))


already = []


def main():
    reddit = praw.Reddit(user_agent='its-fewer-ya-dingus',
                         client_id='', client_secret="",
                         username='its_fewer_ya_dingus', password='')
    print("logged in")
    while True:
        for comment in reddit.subreddit('all').stream.comments():
            if comment.fullname in already or 'bot' in comment.author.name or comment.author.name == 'AutoModerator':
                continue
            try:
                process_comment(comment)
            except Exception as e:
                print(e)
                time.sleep(60 * 1)
            else:
                already.append(comment.fullname)
                time.sleep(5)
        time.sleep(2)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(60)
