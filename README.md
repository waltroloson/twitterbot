# TwitterBot #

This README file documents the deployment and usage of TwitterBot. This software was developed by Jacek Aleksander Gruca for Walter Roloson as part of their contract concluded electronically in May 2016.

### What does TwitterBot do? ###

TwitterBot is a bot that follows handles on a specified list according to the following logic defined below.

This project called TwitterBot is an attempt to create a bot that will carry out the following tasks:

i. Follow handles on a specific list.
i. Track when they were last followed.
i. Not follow anyone followed in the past year.
i. Not follow anyone already following my handle.
i. Unfollow the person after 30 days.
i. Limit follows per day to 50.
i. If already following a person that is not following my handle and they have not been followed in the past year, unfollow them and then re-follow them in 30 days.

### What does a single TwitterBot execution entail? ###

The following list always assume that if no further action is to be taken by the current step, the processing should continue to the next step.

a. Maintain a queue of handles to be followed.
a. Read input file as list of handles (which might have changed from previous execution).
a. Identify handles removed from the list.
a. Remove those items from the queue.
a. Identify handles added to the list.
a. Add those items to the end of the queue.
a. Unfollow all handles followed in the last 30 days or more.
a. Follow all handles marked as unfollowed-on-purpose 30 days or more ago.
a. Take a handle from the queue head.
a. Check if the handle taken from the queue was followed in the past year. If yes: discard, add to the back of the queue, and take another item from the queue head.
a. Check if the handle taken from the queue follows my handle. If yes: discard, add to the back of the queue, and take another item from the queue head.
a. Check if we are already following that handle. If yes then:
    i. unfollow that handle and mark as unfollowed-on-purpose,
    i. add it to the back of the queue,
    i. take another item from the queue head.
a. Check if already followed 50 handles today. If yes: conclude execution.
a. Follow that handle.
a. Add that handle to the back of the queue.
a. Take another item from the queue head and repeat.

### What is TwitterBot's execution frequency? ###

The bot will probably be invoked once a day.

### What are TwitterBot's implementation details? ###

TwitterBot is implemented in Python 2.7. It makes use of MongoDB for persistence storage.

### Are there any other similar projects? ###

Similar publicly available projects are:

1. <https://pypi.python.org/pypi/TwitterFollowBot/v2.0>
1. <https://github.com/rhiever/TwitterFollowBot>
1. <https://github.com/ProgrammingforMarketers/grow-twitter-following>
