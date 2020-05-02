import os
import sys
import time
import requests
import argparse

from bs4 import BeautifulSoup 

import random
import string 


from re import findall
from urllib.request import urlopen

import json


class Instagram(object):

    def __init__(self, username):
        self.username = username

    def RetrieveProfileInformation(self):
        url = "http://www.instagram.com/" + self.username
        print("\n\nDownloading Details of " + self.username)
        response = None
        try:
            response = requests.get(url)
        except Exception as e:
            print(repr(e))
            sys.exit(1)
        
        if response.status_code != 200:
            print("Non success status code returned "+str(response.status_code))
            sys.exit(1)
        
        else:

            bsoup = BeautifulSoup(response.text, 'html.parser')
            
            scylla_scripts = bsoup.find_all('script', attrs={'type': 'text/javascript'})
            tr = str(scylla_scripts[3])[51:-10]
            self.t_data = json.loads(tr)
            self.bsoup_data = self.t_data['entry_data']['ProfilePage'][0]['graphql']['user']
            opt = '''
        > Username                :: {} 
        > Name                    :: {} 
        > Url                     :: {}
        > Followers               :: {} 
        > Following               :: {}
        > # of posts              :: {}
        > Biography               :: {}
        > External url            :: {} 
        > Private                 :: {}
        > Verified                :: {}
        > Business account        :: {} 
        > Connected To Facebook   :: {}
        > Joined recently         :: {}
        > Business category       :: {}
        > Profile Picture         :: {}
            '''.format(str(self.bsoup_data['username']), str(self.bsoup_data['full_name']), 
            str("instagram.com/%s" % self.username), str(self.bsoup_data['edge_followed_by']['count']),
            str(self.bsoup_data['edge_follow']['count']), str(self.bsoup_data['edge_owner_to_timeline_media']['count']),
            str(self.bsoup_data['biography']), str(self.bsoup_data['external_url']),
            str(self.bsoup_data['is_private']), str(self.bsoup_data['is_verified']), str(self.bsoup_data['is_business_account']),
            str(self.bsoup_data['connected_fb_page']), str(self.bsoup_data['is_joined_recently']),
            str(self.bsoup_data['business_category_name']), str(self.bsoup_data['profile_pic_url_hd']))

        return opt


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-in", 
                        "--instagram",
                        type=str,
                        help="return the information associated with specified instagram account",
                        )

    args = parser.parse_args()

    if args.instagram:
        print("Attempting To Gather Account Information")
        try:
            print(Instagram(args.instagram).RetrieveProfileInformation())
        except KeyboardInterrupt as ki:
            cprint("\tExiting")
            sys.exit(1)

if __name__ == "__main__":
    main() 