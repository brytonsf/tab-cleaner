from appscript import *
import re
import datetime
import random
import string
import os
from dbmodel import DBModel
from model import TabStorageOperation
from utils import *


# This program has a primary function/purpose/tool:
# It lets you close out all your tabs and store all of them.
#
# This closing-out operation, the accounting-for of all tabs, is done in some moment.
# The datetime of such a running of this program is mapped to all the tabs it captures.
#
# You can then do a few things over your tabs:
# - Retrieve all the URLs, possibly filtering out various unneeded ones
# - View all unique domains for an operation
#
# One thing we want though, in general or more long term, is the ability to like more truly account for
#   all these tabs by integrating them into one's PKM. IDK. What else should we add here?


class Tab():
	def __init__(self, appleScriptObject):
		self.url = appleScriptObject.URL()
		self.title = appleScriptObject.title()
		self.domain = extract_domain(self.url)
		self.appleScriptObject = appleScriptObject

	def __str__(self):
		return f"{self.domain} : {self.title}"


def read_tabs_from_topmost_open_chrome_instance(close = False):
    tabs_raw = app('Google Chrome').windows[0].tabs()
    tabs = [Tab(obj) for obj in tabs_raw]
    store = create_domain_keyed_tab_store(tabs)

    print("\n")
    print(f"{len(tabs)} total tabs.")
    print(f"{len(store.keys())} unique domains.")

    if close:
        for tab in tabs:
            tab.appleScriptObject.close()

    return tabs

# Load all operations from db, and count total number of tabs (with titles) across all operations
def total_tab_count_from_db():
    operations = TabStorageOperation.find_all()
    count = 0
    for op in operations:
        if hasattr(op, 'titles') and op.titles:
            count += len(op.titles)
        elif hasattr(op, 'urls') and op.urls:  # fallback if titles not present
            count += len(op.urls)
    return count



if __name__ == "__main__":
    print("Options (type number & enter to perform action):")
    print("1. Capture all tabs – records all URLs under this datetime for all open Chrome windows.")
    print("\tOnly opened, not minimized windows, will be captured. This will close out all open tabs.")


    action = input("Action: ")

    if action == "1":
        all_tabs = []
        close = True
        tabs = read_tabs_from_topmost_open_chrome_instance(close = close)
        all_tabs.extend(tabs)

        while True:
            go = input("Again? y/n (or enter): ")
            if go == "y" or go == "":
                tabs = read_tabs_from_topmost_open_chrome_instance(close = close)
                all_tabs.extend(tabs)
            elif go == "n":
                break
            else:
                continue

        print("Finished accumulating tabs, storing in DB...")

        urls = []
        titles = []
        for tab in all_tabs:
            if tab is not None: # Not sure why tab would be none, but it has happened. Might be a new tab.
                urls.append(tab.url)
                titles.append(tab.title)

        result = TabStorageOperation(
            urls = urls,
            titles = titles
        )
        result.create()

        print("Done!")


    else:
        print("Invalid action, exiting.")
