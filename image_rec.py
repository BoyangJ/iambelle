import json
import random
import os
from clarifai.rest import ClarifaiApp


acceptable_confidence = 0.8
clothing_confidence = 0.6
app = ClarifaiApp(os.environ['CLARIFAI_APP_ID'], os.environ['CLARIFAI_APP_SECRET'])


# Relevant Clarif.ai tags for our categories
masculine_tags = ["boy", "man", "male", "people"]
feminine_tags = ["woman", "girl", "female", "lady"]
animal_tags = ["dog", "puppy", "cat", "kitten", "squirrel", "fish", "bird", "baby"]
hair_colours = ["blond", "brunette", "redhead", "ginger"]
outside_tags = ["nature", "outdoors", "grass", "park", "tree", "wood", "sky", "environment"]
happy_tags = ["smile", "happy", "joy", "delight"]


def keywithmaxval(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


# Returns the the main focus of the photo.
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


# Checks if eyes are prominent in the photo.
def is_eyes(concepts):
    eyes = "False"
    confidence = -1.0
    for attribute in concepts:
        if attribute["name"] == "eye":
            confidence = attribute["value"]
            if confidence > acceptable_confidence:
                eyes = True
            break
    return eyes, confidence


# Checks if happiness is a prominent feature
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


# Checks if hair colour is a prominent feature
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


# Returns the most likely category for a photo.
def get_top_tag(concepts):
    clothing = "unknown"
    confidence = -1.0
    if confidence > clothing_confidence:
        clothing = concepts[0]["name"]
        confidence = concepts[0]["value"]
    return clothing, confidence

# Checks if the photo is likely to be outdoors
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

    tweet_template_file = open("tweet_template.json", 'r', encoding="utf8")
    tweet_template = json.load(tweet_template_file)

    general_tags = app.tag_urls([URL], model='general-v1.3')
    general_concepts = general_tags['outputs'][0]['data']['concepts']

    subject, confidence = get_subject(general_concepts)

    # Authors a tweet based off what is believed to be in the photo
    final_tweet = ""
    if subject == "group":
        final_tweet = tweet_template["group"][random.randrange(0, len(tweet_template["group"]))] + "  " + tweet_template["icons"][random.randrange(0,len(tweet_template["icons"]))]
    elif subject in animal_tags:
        final_tweet = (tweet_template["pets"][random.randrange(0, len(tweet_template["pets"]))] + "  " + tweet_template["icons"][random.randrange(0, len(tweet_template["icons"]))]).replace("$", subject.lower())
    elif subject == "female" or subject == "male":
        apparel_tags = app.tag_urls([URL], model='apparel')
        apparel_concepts = apparel_tags['outputs'][0]['data']['concepts']

        # Populates a map with confidences and values for photo categories
        confidence_map = {}
        eyes, eyes_confidence = is_eyes(general_concepts)
        hair_colour, hair_confidence = get_hair_colour(general_concepts)
        happy, happy_confidence = is_happy(general_concepts)
        clothes, clothes_confidence = get_top_tag(apparel_concepts)
        outside, outside_confidence = is_outside(general_concepts)

        # Quickly just ensures that watches are not over reported
        if clothes.lower() == "men's watch" or clothes.lower == "women's watch":
            if not (clothing_confidence > 0.95):
                clothes.confidence = -1.0

        confidence_map["eyes"] = eyes_confidence
        confidence_map["hair"] = hair_confidence
        confidence_map["happy"] = happy_confidence
        confidence_map["clothes"] = clothes_confidence + 0.1
        confidence_map["outside"] = outside_confidence
        confidence_map["unknown"] = 0

        largest = keywithmaxval(confidence_map)
        if largest == "eyes":
            final_tweet = tweet_template["single"]["Eye"][random.randrange(0, len(tweet_template["single"]["Eye"]))]
        elif largest == "hair":
            final_tweet = tweet_template["single"]["Hair"][random.randrange(0, len(tweet_template["single"]["Hair"]))].replace("$", hair_colour.lower())
        elif largest == "happy":
            final_tweet = tweet_template["single"]["Happy"][random.randrange(0, len(tweet_template["single"]["Happy"]))]
        elif largest == "outside":
            final_tweet = tweet_template["single"]["Outside"][random.randrange(0, len(tweet_template["single"]["Outside"]))]
        elif largest == "clothes":
            final_tweet = tweet_template["single"]["Clothes"][random.randrange(0, len(tweet_template["single"]["Clothes"]))].replace("$", clothes.lower())
        else:
            final_tweet = tweet_template["single"]["Default"][random.randrange(0, len(tweet_template["single"]["Default"]))]
        final_tweet + "  " + tweet_template["icons"][random.randrange(0,len(tweet_template["icons"]))]
    return final_tweet

#print(authorTweet('https://headshotcrew.com/sites/all/themes/hsc/images/maurice.jpg'))