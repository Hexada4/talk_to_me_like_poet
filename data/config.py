import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
LINKS = os.getenv('LINKS').split(',') # os.getenv() always returns str,
                                      # so split() is to get list from string
