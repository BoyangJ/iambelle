import json
import random
import os
from clarifai.rest import ClarifaiApp


acceptable_confidence = 0.8
clothing_confidence = 0.6
app = ClarifaiApp(os.environ['CLARIFAI_APP_ID'], os.environ['CLARIFAI_APP_SECRET'])
masculine_tags = ["boy", "man", "male"]
feminine_tags = ["woman", "girl", "female", "lady"]
animal_tags = ["dog", "puppy", "cat", "kitten", "squirrel", "fish", "bird", "baby"]
hair_colours = ["blond", "brunette", "redhead", "ginger"]
outside_tags = ["nature", "outdoors", "grass", "park", "tree", "wood", "sky", "environment"]
happy_tags = ["smile", "happy", "joy", "delight"]


def keywithmaxval(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

def get_subject(concepts):
    subject = "unknown"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] == "group":
            confidence = attribute["value"]
            if confidence < acceptable_confidence:
                break
            subject = "group"
            break
        if attribute["name"] in masculine_tags:
            confidence = attribute["value"]
            if confidence < acceptable_confidence:
                break
            subject = "male"
            break
        if attribute["name"] in feminine_tags:
            confidence = attribute["value"]
            if confidence < acceptable_confidence:
                break
            subject = "female"
            break
        if attribute["name"] in animal_tags:
            confidence = attribute["value"]
            if confidence < acceptable_confidence:
                break
            subject = attribute["name"]
            break
    return subject, confidence

def is_eyes(concepts):
    eyes = "False"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] == "smile":
            confidence = attribute["value"]
            if confidence > acceptable_confidence:
                eyes = True
            break
    return eyes, confidence

def is_happy(concepts):
    happy = "False"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] in happy_tags:
            confidence = attribute["value"]
            if confidence > acceptable_confidence:
                happy = True
            break
    return happy, confidence

def is_smiling(concepts):
    smiling = "False"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] == "smile":
            confidence = attribute["value"]
            if confidence > acceptable_confidence:
                smiling = True
            break
    return smiling, confidence

def get_hair_colour(concepts):
    hair_colour = "unknown"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] in hair_colours:
            confidence = attribute["value"]
            if confidence < acceptable_confidence:
                break
            hair_colour = attribute["name"]
            break
    return hair_colour, confidence

def get_clothing(concepts):
    clothing = "unknown"
    confidence = -1.0
    if confidence > clothing_confidence:
        clothing = concepts[0]["name"]
        confidence = concepts[0]["value"]
    return clothing, confidence

def is_outside(concepts):
    outside = "False"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] in outside_tags:
            confidence = attribute["value"]
        if confidence > acceptable_confidence:
            outside = True
            break
    return outside, confidence

def authorTweet(URL):

    tweet_file = open("tweet_template.json", 'r', encoding="utf8")
    tweets = json.load(tweet_file)


    general_tags = app.tag_urls([URL], model='general-v1.3')
    general_concepts = general_tags['outputs'][0]['data']['concepts']

    subject, confidence = get_subject(general_concepts)
    #print(general_concepts)

    #print(subject + "  " + str(confidence))
    final_tweet = ""
    if subject == "group":
        final_tweet = tweets["group"][random.randrange(0, 3)] + "  " + tweets["icons"][random.randrange(0,10)]
    elif subject in animal_tags:
        final_tweet = (tweets["pets"][random.randrange(0, 3)] + "  " + tweets["icons"][random.randrange(0, 10)]).replace("$", subject)
    elif subject == "female" or subject == "male":
        apparel_tags = app.tag_urls([URL], model='apparel')
        apparel_concepts = apparel_tags['outputs'][0]['data']['concepts']
        #print(apparel_concepts)
        dict = {}
        eyes, eyes_confidence = is_eyes(general_concepts)
        hair_colour, hair_confidence = get_hair_colour(general_concepts)
        happy, happy_confidence = is_happy(general_concepts)
        clothes, clothes_confidence = get_clothing(apparel_concepts)
        outside, outside_confidence = is_outside(general_concepts)
        #print(eyes_confidence)
        #print(hair_confidence)
        #print(happy_confidence)
        #print(clothes_confidence)
        #print(outside_confidence)
        dict["eyes"] = eyes_confidence
        dict["hair"] = hair_confidence
        dict["happy"] = happy_confidence
        dict["clothes"] = clothes_confidence + 0.1
        dict["outside"] = outside_confidence
        dict["unknown"] = 0

        largest = keywithmaxval(dict)
        #print(largest)
        if largest == "eyes":
            final_tweet = tweets["single"]["Eye"][random.randrange(0, len(tweets["single"]["Eye"]))]
        elif largest == "hair":
            final_tweet = tweets["single"]["Hair"][random.randrange(0, len(tweets["single"]["Hair"]))].replace("$", hair_colour)
        elif largest == "happy":
            final_tweet = tweets["single"]["Happy"][random.randrange(0, len(tweets["single"]["Happy"]))]
        elif largest == "outside":
            final_tweet = tweets["single"]["Outside"][random.randrange(0, len(tweets["single"]["Outside"]))]
        elif largest == "clothes":
            final_tweet = tweets["single"]["Clothes"][random.randrange(0, len(tweets["single"]["Clothes"]))].replace("$", clothes)
        else:
            final_tweet = tweets["single"]["Default"][random.randrange(0, len(tweets["single"]["Default"]))]
        final_tweet + "  " + tweets["icons"][random.randrange(0,len(tweets["icons"]))]
    return final_tweet
