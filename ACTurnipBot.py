import praw
import re
from datetime import datetime
import time
import random
import config

class ACTurnipBot():

    def __init__(self):
        print("ACTurnipBot Initionalization started...")
        self.start_time = datetime.now()
        self.invites_requested = 0

        # settings can be changed in configure.py (additional info also in project's README.txt)
        #importing settings from config file
        self.possible_replys_list = config.possible_replys_list
        self.key_word_dict = config.key_word_dict
        self.minimum_price = config.minimum_price
        self.max_comments = config.max_comments
       
        # create python reddit api wrapper (praw) object
        self.reddit = praw.Reddit(client_id=config.client_id, client_secret=config.account_secret, user_agent=config.user_agent, username='GreatSpeedyDragon', password='ze6f3eZt1Uzf')
        # create subreddit object
        self.subreddit = self.reddit.subreddit('acturnips')

    def findLargestNumber(self, number_list):
        # params: number_list is a list with 0 or more ints
        # return: the largest number from number_list

        biggest_number = 0
        
        for number in number_list:
            current_number = int(number)
            if (current_number > biggest_number):
                biggest_number = current_number
        
        return biggest_number

    def findKeyWords(self, post_body):
        # params: post_body will contain the reddit post as a string
        # return: a string containing the key words that were checked for and found.

        requested_key_words = ""
        post_body_upper = post_body.upper()
        
        # check the post body for every key, if a key is found then add the keys value to requested_key_words
        for key in self.key_word_dict:
            if self.key_word_dict[key] in post_body_upper:
                requested_key_words = requested_key_words + self.key_word_dict[key] 
        
        return (requested_key_words)        

    def getRandomReply(self):
        # return: a string of one of the possible

        statement_count = len(self.possible_replys_list)
        random_choice = random.randint(0,(statement_count-1))

        return (self.possible_replys_list[random_choice])

    def buildReplyMessage(self, post_body):
        # params: post_body is the body of a reddit post
        # return: message as a string containing a random reply and requested keywords
        
        key_words = self.findKeyWords(post_body)

        # combine a random reply from the list and 
        # the keywords to produce a realistic looking reply
        reply_text = (self.getRandomReply() + key_words)

        return reply_text

    def postReply(self, submission):
        # params: submission is a submission object. it contains all data from a reddit post.
        # method will post a reply requesting to be invited to the posters island
        
        message = self.buildReplyMessage(submission.selftext)

        # submit the reply
        try:
            # submit the reply
            submission.reply(message)
            print("replied to post " + submission.title)

            self.invites_requested = self.invites_requested + 1
            print("Posted reply.")
        except:
            print("ERROR: Reply submission failed. Possibly exceeded the reddit post rate limit...")  

    def doubleCheckPrice(self, title):
        # params: title is the title of the reddit post
        # return: the price found in the title.

        # this method double checks the title for the price of bells in the title.
        # some people make the numbers hard to read via obfuscation and it cant be read as a normal int.
        
        price = 0
        title_upper = title.upper()

        if ("FOR THREE" in title_upper or "AT THREE" in title_upper or "FOR 3" in title_upper or "AT 3" in title_upper):
            # might be 300
            print("double checked, might be 300")
            price = 300
        if ("FOR FOUR" in title_upper or "AT FOUR" in title_upper or "FOR 4" in title_upper or "AT 4" in title_upper):
            # might be 400
            print("double checked, might be 400")
            price = 400
        if ("FOR FIVE" in title_upper or "AT FIVE" in title_upper or "FOR 5" in title_upper or "AT 5" in title_upper):
            # might be 500
            print("double checked, might be 500")
            price = 500
        if ("FOR SIX" in title_upper or "AT SIX" in title_upper or "FOR 6" in title_upper or "AT 6" in title_upper):
            # might be 600
            print("double checked, might be 600")
            price = 600
        
        return price
        
    def findBellAmount(self, title):
        # params: title is the title of the post
        # return: amount of bells that is being offered per turnip
        # method will find the amount of bells being advertised in the title.
        
        # check if there are ints in the title
        if (re.findall('\d+', title) != None):
            numbers = re.findall('\d+', title)
            bell_amount = self.findLargestNumber(numbers) # make sure only the largest int in the title is used
        else:
            bell_amount = 0
            
        if (bell_amount < 50):
            # some users use obfuscation to hide the sale price from bots, so it will search a
            # second time for the price if its not found to be high enough after the first scan.
            double_checked_amount = self.doubleCheckPrice(title)
            
            bell_amount = double_checked_amount
        
        return bell_amount

    def printSubmissionInfo(self, submission):
        # params: submission is a submission object. it contains all data from a reddit post.
        # prints the data from a submission
        print("\nPost Title: ", submission.title)
        bells = self.findBellAmount(submission.title)
        print("Amount of Bells: ", bells)
                            
        print("Post Score: ", submission.score)  # Output: the submission's score
        print("Submission id: ", submission.id)     # Output: the submission's ID

        print("Submission time UTC: ", datetime.fromtimestamp(submission.created_utc))
        print("number of comments: ", submission.num_comments)

    def checkSubmission(self, submission):
        # params: submission is a submission object. it contains all data from a reddit post.
        # checks if the submission meets the set values desired
        valid_submission = True
        bells = self.findBellAmount(submission.title)

        if(int(submission.num_comments) > self.max_comments):
            print("The comment number surpasses the set threshold.")
            valid_submission = False
        if(bells < self.minimum_price):
            print("The price does not meet the set threshold.")
            valid_submission = False
        if("turnip.exchange/island" in str(submission.selftext) or "https://turnip.exchange" in str(submission.selftext)):
            print("Contains https://turnip.exchange/island so won't get invited from replys")
            valid_submission = False
        if("LOOKING TO SELL" in str(submission.title).upper()):
            print("person is looking to sell their turnips")
            valid_submission = False
        
        return(valid_submission)
        
    def runScanner(self):
        # this method will continuously scan for new posts

        reviewed_submissions = []

        while True:
            print("Scanning...\ninvites requested: " , self.invites_requested , "\ntime running: " ,((datetime.now()) - self.start_time))
            
            # get the 4 most recent posts
            recent_posts = self.subreddit.new(limit=4)

            # check each of the recent posts
            for submission in recent_posts:
                if (submission.id not in reviewed_submissions):
                    # print the submission that was reviewed
                    self.printSubmissionInfo(submission)

                    # check if submission meets search criteria
                    if(self.checkSubmission(submission)):
                        self.postReply(submission)

                    # add submission to the reviewed list
                    reviewed_submissions.append(submission.id)
            # must sleep otherwise the program will exceed api request limit.  
            time.sleep(5)