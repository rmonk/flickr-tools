#!/bin/env python3

import flickrapi
import json
import argparse

CONFIGFILE="config.json"


parser = argparse.ArgumentParser()

parser.add_argument("search", help="String to search for", default=None)
parser.add_argument("-c", "--count", help="How many items to return", default=10)

args = parser.parse_args()

with open(CONFIGFILE, "r") as configfd:
    config = json.load(configfd)

flickr = flickrapi.FlickrAPI(config["apikey"], config["secret"], format='parsed-json')

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='write'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='write')
    print("Authorization URL: {}".format(authorize_url))

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

print('Step 2: use Flickr')
userid = flickr.urls.lookupUser(url=config["profile_url"])["user"]["id"]

page = 1
photos = flickr.photos.search(user_id = userid, text = args.search, per_page = args.count, page = page)
for photo in photos["photos"]["photo"]:
    print(json.dumps(photo, indent=2))
    photo_info = flickr.photos.getInfo(photo_id=photo["id"])
    print(json.dumps(photo_info, indent=2))
