# reddit account setup information: https://www.reddit.com/wiki/api
# Your account flair for r/acturnips must be set properly to post: https://www.reddit.com/r/acturnips/wiki/flair

# reddit account info
username='reddit_username' # Change Required
password='reddit_password' # Change Required
account_secret = "reddit_account_secret" # Change Required
# link for info on user_agent: https://github.com/reddit-archive/reddit/wiki/API#rules
user_agent = "unique string that reddit tells you how to assemble" # Change Required
client_id='reddit_client_id' # Change Required

# search parameters
minimum_price = 390
max_comments = 75

# list of replys to keep the bot posts differing some
possible_replys_list = [
    "Hey I'd Love to get in. Also Thanks for hosting this, much appreciated. ",
    "Hi, I'd love an invite. Thanks! ",
    "Thanks for doing this! I'd love an invite. ",
    "I would like an invite when there is room. Thanks! ",
    "Would really appricate an invite. Also thanks for doing this. ",
    "Thanks for hosting this dude! Id like an invite when possible. "
]

# words people add to their posts to screen out bots 
# the keys value will be added to the bots reply.
key_word_dict = {
    "FRUIT": "Apple",
    "FAVORITE VILLAGER": " Tabby",
    "FAVORITE SEASON": " Summer",
    "FAVORITE ANIMAL": " Dogs",
    "FAVORITE MOVIE": " Star Wars VI",
    "KK SONG": " KK bubblegum",
    "FAVORITE FLOWER": " daisy",
    "FAVORITE COLOR": " blue",
    "IN-GAME NAME": " #USERNAME",
    "IN GAME NAME": " #USERNAME",
}