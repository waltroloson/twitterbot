# TwitterBot #

This README file documents the deployment and usage of TwitterBot. This software was developed by Jacek Aleksander Gruca for Walter Roloson as part of their contract concluded electronically in May 2016.

### What does TwitterBot do? ###

TwitterBot is a bot that follows handles on a specified list according to the logic defined below.

1. Follow handles on a specific list.
1. Track when they were last followed.
1. Not follow anyone followed in the past year.
1. Not follow anyone already following my handle.
1. Unfollow the person after 30 days.
1. Process no more than 50 items in the queue per each invocation.
1. If already following a person that is not following my handle and they have not been followed in the past year, unfollow them and then re-follow them in 30 days.

### What are TwitterBot's implementation details? ###

TwitterBot is implemented in Python 2.7. It makes use of MongoDB for persistence storage and interacts with the Twitter API.

### How do I get set up? ###

1. Make sure you have Python 2.7, python-dev/python-devel and pip installed.
1. Execute the following commands:
```sh
pip install pandas
pip install tweepy
pip install pymongo
```

### How do I configure TwitterBot? ###

The configuration of TwitterBot is stored in file config.ini. This file contains descriptive comments so proceed there if you want to amend configuration.

You will need to set up a Twitter application. You can create one here: <https://apps.twitter.com/>. Once you have it created navigate to the "Keys and Access Tokens" section for your Consumer Key, Consumer Secret, Access Token and Access Token Secret. These items should be input into the config.ini file.

### How do I begin with TwitterBot? ###

In the command line enter the directory containing this README file and type:
```sh
$ python followHandles.py -h
```

This will output the usage details. The parameter to specify is an input file with handles to be processed.

### What does a single TwitterBot execution entail? ###

1. At the beginning TwitterBot will check whether the queue it maintains and the input list of handles is the same. If it is the same, it will proceed carrying out the logic described above. If there are differences between the queue and the list, it will take the following actions:
  1. Items in the input list, which are missing from the queue, will be added to the queue.
  1. Items in the queue, which are not in the input list, will be removed from the queue.
  1. Please note that any items being followed will not be unfollowed when removed from the queue in the above step. (This behaviou may be amended)
1. TwitterBot is limited by Twitter API rate limits defined here <https://dev.twitter.com/rest/public/rate-limits>. This means that TwitterBot will pause after it has reached any of the limits and sleep for the required number of minutes before processing further. (This is not yet implemented)

### What is TwitterBot's execution frequency? ###

The bot will probably be invoked once a day.

### Are there any other similar projects? ###

Similar publicly available projects are:

1. <https://pypi.python.org/pypi/TwitterFollowBot/v2.0>
1. <https://github.com/rhiever/TwitterFollowBot>
1. <https://github.com/ProgrammingforMarketers/grow-twitter-following>

### Who do I talk to? ###

Please contact Jacek Aleksander Gruca with any issues, questions or comments.
