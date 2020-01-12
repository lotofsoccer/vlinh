from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import UserUtteranceReverted
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted

import requests
import json
from bs4 import BeautifulSoup
from pyvi import ViTokenizer, ViPosTagger
import feedparser

def name_cap(text):
    tarr = text.split()
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    return ' '.join(tarr)

class action_save_cust_info(Action):
    def name(self):
        return 'action_save_cust_info'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
        cust_sex = next(tracker.get_latest_entity_values("cust_sex"), None)
        bot_position = "SHB"

        if (cust_sex is  None):
            cust_sex = "Quý khách"

        if (cust_sex == "anh") | (cust_sex == "chị"):
           bot_position = "em"
        elif (cust_sex == "cô") | (cust_sex == "chú"):
            bot_position = "cháu"
        else:
            cust_sex = "Quý khách"
            bot_position = "SHB"

        if not cust_name:
            #dispatcher.utter_template("utter_greet_name",tracker)
            return []

        print (name_cap(cust_name))
        return [SlotSet('cust_name', " "+name_cap(cust_name)),SlotSet('cust_sex', name_cap(cust_sex)),SlotSet('bot_position', name_cap(bot_position))]

class action_save_mobile_no(Action):
    def name(self):
        return 'action_save_mobile_no'

    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        print(user_id)
        mobile_no = next(tracker.get_latest_entity_values("inp_number"), None)

        if not mobile_no:
            return  [UserUtteranceReverted()]

        mobile_no = mobile_no.replace(" ","")
        #print (cust_name)
        return [SlotSet('mobile_no', mobile_no)]



class action_reset_slot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("transfer_nick", None),SlotSet("transfer_amount", None),SlotSet("transfer_amount_unit", None)]


# Ham lay ket qua so xo va tra ve. Ten ham la action_get_lottery
class action_get_lottery(Action):
   def name(self):
            # Doan nay khai bao giong het ten ham ben tren la okie
          return 'action_get_lottery'
   def run(self, dispatcher, tracker, domain):
            # Khai bao dia chi luu tru ket qua so xo. O day lam vi du nen minh lay ket qua SX Mien Bac
            url = 'https://xskt.com.vn/rss-feed/mien-bac-xsmb.rss'
            # Tien hanh lay thong tin tu URL
            feed_cnt = feedparser.parse(url)
            # Lay ket qua so xo moi nhat
            first_node = feed_cnt['entries']
            # Lay thong tin ve ngay va chi tiet cac giai
            return_msg = first_node[0]['title'] + "\n" + first_node[0]['description']
            # Tra ve cho nguoi dung
            dispatcher.utter_message(return_msg)
            return []