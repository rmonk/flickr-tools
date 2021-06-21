#!/bin/env python3

import json
import flickrapi

CONFIGFILE="config.json"

def authenticate():
    with open(CONFIGFILE, "r") as configfd:
        config = json.load(configfd)

    flickr = flickrapi.FlickrAPI(config["apikey"], config["secret"], format='parsed-json')

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

        
    return flickr
