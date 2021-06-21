#!/bin/env python3

import json
import easyflickr


def jprint(item):
    print(json.dumps(item, indent=2))

flickr = easyflickr.authenticate()

sets = flickr.photosets.getList()["photosets"]

