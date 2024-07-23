# -*- coding: utf-8 -*-
"""
Created on Tue July  23 19:46:08 2024

@author: LTB122
"""
import random
from Player import Player

###
# This player makes all choices base on LLM
###

import google.generativeai as genai #import library
import time

def get_response(prompt): #function to generate output
    genai.configure(api_key="AIzaSyAz3AVttzNbdcJr4bnKkfFG2pV5-cq1ttI") #use gemini api
    generation_config = {
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 40
    }
    #set the safety infor
    safety_settings = [
        {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    #create a model
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)
    convo = model.start_chat() #start to chat
    try:
        convo.send_message(prompt) #ask for the answer
    except:
        time.sleep(5)
        convo.send_message(prompt)
    output = convo.last.text #get the output
    return output #return the output

def choose_option(target, hand):
    prompt = "Choose one word from the following words: 0. "
    prompt+= hand[0]


    for i in range(1,len(hand)):
        prompt+= ", "+ str(i) + ". " + hand[i]


    prompt+= ". Which word best fits the adjective: '"+ target + "'? Please select and return the index number of the chosen word on a single line."
    res = get_response(prompt)
    print(res)
    bang_anh_xa = str.maketrans("", "", ".,:!*#()")


    # Apply a mapping table to the string to remove special characters.
    chuoi_sau_khi_xoa = res.translate(bang_anh_xa)


    # Split the string into words.
    tach_tu = chuoi_sau_khi_xoa.split()


    # Filter and retrieve numbers from a list of words.
    so = [tu for tu in tach_tu if tu.isdigit()]


    # Convert an array containing string numbers into an array of integers.
    mang_so = list(map(int, so))


    ans = 0
    # Check the array of numbers and select the appropriate word.
    for i in range(0,len(mang_so)):
        if(mang_so[i]>=0 and mang_so[i]<len(hand)):
            ans = mang_so[i]
            break

    return ans


class TestPlayer(Player):

    PLAYER_NAME = "Test Player" # Choose a unique name for your player
    
    def __init__(self):
        super().__init__(self.PLAYER_NAME)


    def choose_card(self, target, hand):
        ### Select the index of the card from the cards list that is closest to target
        return choose_option(target, hand)
    
    
    def judge_card(self, target, player_cards):
        ### Select the card that is closest to target
        return player_cards[choose_option(target, player_cards)]
        
    
    def process_results(self, result):
        ### Handle results returned from server
        print("Result", result)

if __name__ == '__main__':
    player = TestPlayer()
    player.run()
