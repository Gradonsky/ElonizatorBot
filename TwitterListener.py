#!/usr/bin/env python
# *************************************
# ****     ELONUS BOTUS CRITICUS   ****
# ****    MONIUS CREATUS TWITTERUS ****
# ****   PRAISE DOGE TO THE MOON   ****
# *************************************
from art import *
from flashtext import KeywordProcessor
import json
import tweepy
import logging
from config import create_api
from urllib3.exceptions import ProtocolError
import time
from py3cw.request import Py3CW
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from uptime import uptime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
keywords = ["The most entertaining outcome is the most likely", "doge", "much wow","dogecoin","Ðogecoin","Buydoge","#dogecoin","much cool","so lisp"]
with open('config.json', 'r') as f:
    config = json.load(f)

    def from_creator(status):
        if hasattr(status, 'retweeted_status'):
            return False
        elif status.in_reply_to_status_id != None:
            return False
        elif status.in_reply_to_screen_name != None:
            return False
        elif status.in_reply_to_user_id != None:
            return False
        else:
            return True


class TwitterListener(tweepy.StreamListener):
    def on_status(self, status):
        if from_creator(status):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_list(keywords)
            logger.info(status.text)
            updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text=status.text)
            keywords_found = keyword_processor.extract_keywords(status.text)
            logger.info(keywords_found)
            if keywords_found:
                logger.info("====== DOGE ALERT ======")
                updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='====== DOGE ALERT ======')
                self.Mooning()
            else:
                try:
                    logger.info("Media found:",True in [medium['type'] == 'photo' for medium in status.entities['media']])
                    logger.info(status.entities["media"][0]["media_url"])
                    updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text=status.entities["media"][0]["media_url"])
                except:
                    logger.info("nothing special here...")
                    updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='nothing special here...')


    def papaElonStreamer(api):
        myStreamListener = TwitterListener()
        elonStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
        updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='Stream started..')
        while True:
            try:
                elonStream.filter(follow=[config['TWITTER_ID']]) # Twitter ID to which bot is listening to
            except (ProtocolError, AttributeError):
                continue
    def Mooning(self):
        logger.info("Passing order...")
        updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='Passing order...')
        try:
            data = p3cw.request(
                entity='bots',
                action='start_new_deal',
                action_id=config['3COMMAS_BOT_ACTION_ID']
            )
        except Exception as e:
            logger.error("Error passing order", exc_info=True)
            updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='Error passing order')
            raise e
        logger.info("3Commas order passed")
        updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='3Commas order passed')

    def startTelegramBot(update, context):
        """Send a message when the command /uptime is issued."""
        update.message.reply_text(uptime()/60)



if __name__ == "__main__":
    tprint("Papa  Elonizator")
    print(r"""     ▄              ▄
                  ▌▒█           ▄▀▒▌
                  ▌▒▒█        ▄▀▒▒▒▐
                 ▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
               ▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
             ▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌
            ▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒▌
            ▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
           ▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄▌
           ▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▌
          ▌▒▀▐▄█▄█▌▄░▀▒▒░░░░░░░░░░▒▒▒▐
          ▐▒▒▐▀▐▀▒░▄▄▒▄▒▒▒▒▒▒░▒░▒░▒▒▒▒▌
          ▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒▒▒░▒░▒░▒▒▐
           ▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒░▒░▒░▒░▒▒▒▌
           ▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▄▒▒▐
            ▀▄▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▄▒▒▒▒▌
              ▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀
                ▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀
                   ▒▒▒▒▒▒▒▒▒▒▀▀""")

    updater = Updater(config['TELEGRAM_BOT_KEY'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("uptime", TwitterListener.startTelegramBot))
    updater.start_polling()
    api = create_api(config['TWITTER_CONSUMER_KEY'],config['TWITTER_CONSUMER_SECRET'],config['TWITTER_ACCESS_TOKEN'],config['TWITTER_ACCESS_SECRET'])
    try:

        p3cw = Py3CW(
            key=config['3COMMAS_API_KEY'],
            secret=config['3COMMAS_API_SECRET'],
            request_options={
                'request_timeout': 10,
                'nr_of_retries': 1,
                'retry_status_codes': [502]
            })
    except Exception as e:
        logger.error("Error connecting API 3Commas", exc_info=True)
        updater.bot.send_message(-float(['TELEGRAM_BOT_GROUP_ID']), text='Error connecting API 3Commas')
        raise e
    logger.info("3Commas API Connected")
    updater.bot.send_message(-float(config['TELEGRAM_BOT_GROUP_ID']), text='APIs Connected')
    TwitterListener.papaElonStreamer(api)
