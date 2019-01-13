#!/usr/bin/env python3
#----------------------------------------------------------------------------
# Author      : Liam Jones
# Description : A simple python web scraper to pull Dribbble content into slack.
#               ...
#----------------------------------------------------------------------------
#

import os
import urllib3
import requests, bs4
import simplejson as json
from datetime import datetime
from bs4 import BeautifulSoup

class Post:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        string = ''
        for k,v in vars(self).items():
            string += k + '=' + str(v) + '\n'

        return string

    def serialize(self):
        amap = {}
        amap['id'] = self.id
        amap['date'] = self.date
        return amap

    def format_slack(self):
        if self.url:
            return '{ "text": "'+ str(self.title) +'", "attachments": [ { "text": "Likes: ' + str(self.likes) + '\nComments: ' + str(self.comments) + '\nAuthor: ' + str(self.author) + '", "image_url": "' + str(self.url) +'" } ] }'
        return '{ "text": "'+self.msg+'", "unfurl_media": true }'

class DribbbleCrawler:
    # -------------------------------------------
    # Purpose: Send the post hooks to slacks API.
    # Passed-in: post object.
    def send(self, post):
        # Put together the POST payload, and save emojis by encode using utf-8
        body = post.format_slack()

        # api_hook = 'https://slack.com/api/chat.postMessage?token=xoxp-155842872885-155048107520-523810353302-6e3a2f35aa4d2a78a80a734b3d2514fa&channel=test&text=\'another test\''
        hook = 'https://hooks.slack.com/services/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'
        # hook = 'https://hooks.slack.com/services/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'

        # Shoot the message to slack using the hook we setup at <workspace>.slack.com
        r = requests.post(hook, headers={'Content-Type': 'application/json'},
                                data=body.encode('utf-8'))

        write_to_file(post)


    def start(self, url):
        page_source = get_source(url)
        # page_source = get_HTML('topPosts.html')

        soup = BeautifulSoup(page_source, 'html.parser')

        # Skip to the posts grouping
        items = soup.select('li.group')

        # Iterate through each of the posts
        for li in items:
            # Get the post ID
            post_id = li['id']

            # TODO: Check that this is not the most recently posted post
            if match_recent(post_id) == True:
                continue

            # Get the post title
            if li.strong:
                post_title = li.strong.get_text().strip()

            # Get author
            if li.h2.a:
                post_author = li.h2.a.get_text()

            # Get post Src
            post_srcset = li.picture.source.get('srcset', None)

            # Get post Likes
            if li.ul.li.a:
                post_likes = li.ul.li.a.get_text()

            # Get Post Comments
            if li.ul.li.a:
                post_comments = li.ul.span.get_text().strip()

            # TODO: Get post views
            post_views = li.ul.get('views', None)

            post = Post(
                id = post_id,
                title = post_title,
                author = post_author,
                url = post_srcset,
                likes = post_likes,
                comments = post_comments,
                views = post_views,
                date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )

            self.send(post)
            print(post)
            break


def get_HTML(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return "".join(lines)


def get_source(url):
    return requests.get(url).text


def write_to_file(post):
    cur_date = datetime.now()

    # if os.path.exists("recent_posts.txt"):
    with open('recent_posts.txt', 'r+') as f:
        line = f.readline()

        list = json.loads(line)
        list.append({'id': post.id, 'date': post.date})

        new_list = []
        for item in list:
            new_date = datetime.strptime(item['date'],"%Y-%m-%d %H:%M:%S")

            if (cur_date - new_date).days < 7:
                new_list.append(item)

        f.seek(0)
        f.write(json.dumps(new_list))
        f.truncate()

        f.close()


def match_recent(post_id):
    if os.path.exists("recent_posts.txt"):
        # Open file and read existing JSON object
        f = open('recent_posts.txt', 'r')
        line = f.readline()
        f.close()

        list = json.loads(line)

        # Check every item for a matching id
        for item in list:
            if item['id'] == post_id:
                return True
        return False
    else:
        print ('hit')
        f = open('recent_posts.txt', 'w+')
        f.write('[]')
        f.close()


if __name__ == "__main__":
    crawler = DribbbleCrawler()
    crawler.start('https://dribbble.com/shots?timeframe=week')
