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

### How do I configure my MongoDB instance? ###

1. Please follow the below commands. A useful resource to refer to is also: <http://www.codexpedia.com/devops/mongodb-authentication-setting/>.

1. First install MongoDB by following the instructions for your operating system. We will assume you installed version 3.2. Ref. <https://docs.mongodb.com/manual/installation/?jmp=footer&_ga=1.175002593.2134140820.1471180198>

1. Then enter the MongoDB shell by typing in the following in the command line:
```sh
$ mongo
```

1. [create-admin-user] Next execute the following commands. Make sure the 'exit' command at the bottom is executed and that the mongo shell exits as a result.
```sh
use admin;
db.createUser(
{
user: "admin",
pwd: "adminPassword",
roles: [ { role: "root", db: "admin" } ]
}
);
exit;
```

1. Shutdown your Mongo instance by following these instructions:
<http://stackoverflow.com/questions/11774887/how-to-stop-mongo-db-in-one-command>.

1. Locate your configuration file `mongod.conf`. It will be in /etc or /usr/local/etc or a similar directory.

1. Edit this file by appending the following lines to it at the bottom. This will disable passwordless login from your localhost workstation, and will always require a password to log in.
```sh
setParameter:
  enableLocalhostAuthBypass: false
security:
  authorization: enabled
```

1. Start your mongo instance again.
```sh
$ mongod --config /path/to/your/config/file/mongod.conf
```

1. If at any step in this whole MongoDB section you get into problems, carry out the following.
    * Go back into the `mongod.conf` file and set the 'enableLocalhostAuthBypass' flag to 'true'.
    * Restart the mongo instance as instructed above.
    * Start up the mongo shell.
    * Proceed again starting at step [create-admin-user] above.

1. Again enter the MongoDB shell by typing in the following in the command line.
```sh
$ mongo
```

1. Execute the following commands. Again make sure the bottom command 'exit' executes and that the mongo shell quits as a result.
```sh
use admin;
db.auth("admin", "adminPassword");
use twitterbot;
db.createUser(
{
user: "twitterbot",
pwd: "twitterbotPassword",
roles: [ { role: "dbAdmin", db: "twitterbot" }, { role: "readWrite", db: "twitterbot" } ]
}
);
exit;
```

1. Then connect to your Mongo DB instance again (by typing `mongo` in the shell) and execute the following commands. Again remember about the 'exit' command.
```sh
use twitterbot;
db.auth('twitterbot','twitterbotPassword');
db.createCollection('queue');
db.createCollection('allhandles');
db.queue.find();
db.allhandles.find();
exit;
```

1. The above commands validate your MongoDB set up. If they fail, don't proceed further but instead try to identify which of the previous steps is causing the problem.

1. Finally set up your MongoDB URI in file config.ini.

### How do I begin with TwitterBot? ###

In the command line enter the directory containing this README file and type:
```sh
$ python followHandles.py -h
```

This will output the usage details. The parameter to specify is an input CSV file with handles to be processed. This file should contain the following columns (same as sample file 'TwitterFollow-Walt.csv' provided):

1. Name.
1. Job.
1. Title.
1. Company. 
1. Linkedin.
1. Twitter.
1. SIQ.
1. Notes.

### What does a single TwitterBot execution entail? ###

1. At the beginning TwitterBot will check whether the queue it maintains and the input list of handles is the same. If it is the same, it will proceed carrying out the logic described above. If there are differences between the queue and the list, it will take the following actions:
  1. Items in the input list, which are missing from the queue, will be added to the queue.
  1. Items in the queue, which are not in the input list, will be removed from the queue.
  1. Please note that any items being followed will not be unfollowed when removed from the queue in the above step. (This behaviour may be amended)
1. TwitterBot is limited by Twitter API rate limits defined here <https://dev.twitter.com/rest/public/rate-limits>. This means that TwitterBot will pause after it has reached any of the limits and sleep for the required number of minutes before processing further.

### What is TwitterBot's execution frequency? ###

The bot will probably be invoked once a day.

### Are there any other similar projects? ###

Similar publicly available projects are:

1. <https://pypi.python.org/pypi/TwitterFollowBot/v2.0>
1. <https://github.com/rhiever/TwitterFollowBot>
1. <https://github.com/ProgrammingforMarketers/grow-twitter-following>

### Who do I talk to? ###

Please contact Jacek Aleksander Gruca with any issues, questions or comments.
