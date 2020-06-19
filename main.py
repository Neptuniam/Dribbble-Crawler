#!/usr/bin/env python3
"""
A simple web crawler using the requests and BeautifulSoup Libraries
This script pulls top posts from the Dribbble site and sends them to my Slack channel through their API
This project includes a makefile to make running easy, but requires a specified unique Slack token

Use 'make help' for more information on the classes and their functions
"""

import os
import requests, bs4, sys
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


    def format_slack(self):
        return '{ "text": "'+ str(self.title) +'", "attachments": [ { "text": "Author: ' + str(self.author) + '\nLikes: ' + str(self.likes) + '\nComments: ' + str(self.comments) + '\nhttps://dribbble.com' + str(self.link) + '", "image_url": "' + str(self.url) +'" } ] }'


class DribbbleCrawler:
    def send(self, post, hook):
        """
        Send the Post object to Slacks API

        Args:
            post: Post object containing all the attributes of the Dribbble post
            hook: Specifies the Slack Hook for the API to send the post to
        """

        # Put together the POST payload, and save emojis by encode using utf-8
        body = post.format_slack()

        # Shoot the message to slack using the hook we setup at <workspace>.slack.com
        r = requests.post(hook, headers={'Content-Type': 'application/json'}, data=body.encode('utf-8'))

        write_to_file(post)


    def start(self, url, hook):
        """
        Performs the actual crawling of the Dribbble top posts page

        Args:
            url: Specifies the url to crawl
            hook: Specifies the Slack Hook for the API to send the post to
        """

        # Get the source code, either from a request of the page or saved html file
        page_source = get_source(url)
        # page_source = get_HTML('pageNew.html')

        # Use BeautifulSoup to nicely skip to the post list
        soup = BeautifulSoup(page_source, 'html.parser')
        # Skip to the posts grouping
        items = soup.select('li.shot-thumbnail')

        # Iterate through each of the posts
        for li in items:
           # Get the post ID
            post_id = li['id']

            # Checks the 'recent_posts.txt' file to check for the current id, if it has been posted, skip to the next post
            if not li or match_recent(post_id) == True:
                continue
            
            # Inner function to sanitize and fetch attributes by HTML element and CSS class
            def select_and_clean(ele, selector):
                selection = ele.select_one(selector)

                return selection.get_text().strip() if selection else None    

            # Get the post title
            post_title = select_and_clean(li, '.shot-title')

            # Get author
            post_author = select_and_clean(li, '.display-name')

            # Get post Src
            post_srcset = li.picture.source.get('srcset', None)

            # Get the ladder end of the link (working link requires the dribbble.com portion too which is added in format_slack())
            post_link = li.a.get('href', None)

            # Get the current number of likes on the post
            likes = select_and_clean(li, '.js-shot-likes-count')

            # Get the current number of comments on the post
            comments = select_and_clean(li, '.js-shot-comments-count')

            post = Post(
                id = post_id,
                title = post_title,
                author = post_author,
                url = post_srcset,
                link = post_link,
                likes = likes,
                comments = comments,
                date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )

            # Send the post to the Slack API and print its attributes to the console
            self.send(post, hook)
            print(post)
            break


def get_HTML(file):
    """
    Retrieves the source code from a specified saved html file

    args:
        file: The Specified html to retrieve the source code from
    """

    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return "".join(lines)


def get_source(url):
    """
    Retrieves the source code from a specified url usign the requests library

    args:
        url: The Specified url to retrieve the source code from
    """

    headers = {}
    headers['X-Requested-With'] = 'XMLHttpRequest'

    return requests.get(url, headers=headers).text


def write_to_file(post):
    """
    Writes the new post to the recent_posts history file to prevent double posting top posts

    args:
        post: The post object to store in history
    """

    # Gets the current date to prevent posts over a week from being stored (prevents massive backlog of posts)
    cur_date = datetime.now()

    with open('recent_posts.txt', 'r+') as f:
        # Read the current history in from the file and load it into the dictionary
        list = json.loads(f.readline())
        # Append the new post
        list.append({'id': post.id, 'date': post.date})

        # Creates a new list ignoring old posts
        # This keeps the history managable, I don't need every post ever posted just the possible repeats
        new_list = []
        for item in list:
            new_date = datetime.strptime(item['date'],"%Y-%m-%d %H:%M:%S")

            if (cur_date - new_date).days < 14:
                new_list.append(item)

        # Overwrite the history file with the new list
        f.seek(0)
        f.write(json.dumps(new_list))
        f.truncate()

        f.close()


def match_recent(post_id):
    """
    Reads the history files and attempts to match the current id

    args:
        post_id: The id of the possible new post to ensure it hasn't already been sent to the Slack Channel

    return: Returns True/False depending on whether or not a match was made (True=Match was made)
    """

    # Ensures that the recent_posts file can be found
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
    # If the file was not found, create it and recall the function
    else:
        f = open('recent_posts.txt', 'w+')
        f.write('[]')
        f.close()
        match_recent(post_id)


if __name__ == "__main__":
    # Ensure we got enough arguements
    if len(sys.argv) < 2:
        sys.exit(1)


    crawler = DribbbleCrawler()
    crawler.start('https://dribbble.com/shots?timeframe=week', sys.argv[1])
