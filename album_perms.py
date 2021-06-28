#!/bin/env python3

import json
import easyflickr

ALBUMS = "albums.json"

with open(ALBUMS, "r") as albumfd:
    albums = json.load(albumfd)

def jprint(item):
    print(json.dumps(item, indent=2))

flickr = easyflickr.authenticate()

sets = flickr.photosets.getList()["photosets"]



for photoset in sets["photoset"]:
    title = photoset["title"]["_content"]
    if title in albums.keys():
        print(f"{photoset['id']} : {title}")
        should_public =  True if "public" in albums[title] else False
        should_family =  True if "family" in albums[title] else False
        should_friends = True if "friends" in albums[title] else False

        photos = flickr.photosets.getPhotos(photoset_id = photoset["id"])
        for photo in photos["photoset"]["photo"]:
            set_perms = False
            if bool(photo["ispublic"]) != should_public:
                set_perms = True
            if bool(photo["isfamily"]) != should_friends:
                set_perms = True
            if bool(photo["isfriend"]) != should_family:
                set_perms = True

            if set_perms:
               flickr.photos.setPerms(photo_id=photo["id"], is_public = int(should_public), is_family = int(should_family), is_friend = int(should_friends))
               print(f"Setting photo_id={photo['id']}, is_public = {int(should_public)}, is_family = {int(should_family)}, is_friend = {int(should_friends)}")

