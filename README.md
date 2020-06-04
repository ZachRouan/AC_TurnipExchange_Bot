# AC_TurnipExchange_Bot

AC_TurnipExchange_Bot is a Python program for quickly replying to new reddit posts on the acturnips 
subreddit that meet your desired search specifications.

## Required Library

This program utilizes the python reddit api wrapper (praw) library.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required library [praw](https://praw.readthedocs.io/en/latest/getting_started/installation.html).

```bash
pip install praw
```

## Usage

Before using this program you must first change some of your [reddit account settings](https://www.reddit.com/wiki/api)

You must also configure the program and account settings in the "ACTurnipBot/config.py" file. Required changes are marked by comments.

Once your reddit account and the program is configured you can start the program with:
```bash
python C:\Users\ThisUser\Desktop\ACTurnipBot\main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
