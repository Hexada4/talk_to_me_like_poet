# Talk to me like a poet

## Introduction

This is a bot, which uses GRU module to predict next word. Data are displayed in a such way to make net think, that it should write poems not just text. 

__The main goal of this project__ is to get acquainted with NLP. The simplest task here is to predict next word, so I've chosen already written model and tried to play around with it.

## Requirements

- Python 3.8.x

## Installation 

1. Clone repository: 
    ```commandline
    git clone https://github.com/jollianreap/talk_to_me_like_poet.git
    ```
2. Create venv:
    ```commandline
   python3.8 -m venv .venv
   ```
   
3. Base requirements:
    ```commandline
   make base-requirements
   ```

## Collecting data and training model

I've created a special file .env to get the links, which will be parsed (only https://slova.org.ru/). 
1. Paste links into config file:
    ```commandline
   LINKS = your, links, with, commas
   ```
2. Run parsing loop:
    ```commandline
   make parse_links
   ```

3. Run training loop:
    ```commandline
   make train
   ```
## Running bot 

Before getting started, you should paste your bot token in .env file. 

1. Installing screen, if not installed:
    ```commandline
   sudo apt install screen
   ```

2. Running model API:
    ```commandline
   screen -d -m python3 lyrics-generator_copy/ml_api.py 
   ```
   
3. Running bot
    ```commandline
   screen -d -m python3 bot.py
   ```
   
4. Verifying 
    ```commandline
   screen -ls
   ```
