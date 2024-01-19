"""
 Copyright (c) 2023. Vili and contributors.

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

import os
import json
from instagram_private_api import Client
from helper import printer, timer


class Scrape:
    """
    Scrapes data from an Instagram account.

    Requires username and password to log in to Instagram.

    Thanks to Instagram Private API, https://pypi.org/project/instagram-private-api/

    :param username: The username of the account to log in to.
    :param password: The password of the account to log in to.
    :param target: The username of the account to scrape.
    """
    @timer.timer
    def __init__(self, username, password, target):
        self.username = username
        self.password = password
        self.scraped_data = None

        temp_dir = '/tmp'
        credentials_file = os.path.join(temp_dir, "dontlookhere.json")
        if os.name == "posix" and not os.path.exists(credentials_file):
            self.save_credentials(username, password)

        try:
            api = Client(username, password)
            data = api.username_info(target)
            printer.info(f"Logged in as '{username}'.")
        except Exception as e:
            printer.error(f"Error : {e}")
            return

        self.print_account_info(data)

    @staticmethod
    def save_credentials(username, password):
        """
        Saves users credentials temporarily in /tmp/

        Warning, credentials are in cleartext.

        :param username: The username of the account.
        :param password: The password of the account.
        """
        if os.name == "posix":
            temp_dir = '/tmp'
            credentials_file = os.path.join(temp_dir, "dontlookhere.json")
            credentials = {"username": username, "password": password}
            with open(credentials_file, "w") as file:
                json.dump(credentials, file)

            printer.info(f"Credentials saved temporarily in {credentials_file}.")
        else:
            printer.warning("Win system! Not saving...")

    @staticmethod
    def safe_get(data, key, default=None):
        """Safely retrieves nested data from dictionaries."""
        keys = key.split('.')
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return default
        return data

    def print_account_info(self, data):
        """Prints account information."""
        try:
            user = data.get('user', {})
            self.scraped_data = {
                'username': user.get('username'),
                'full_name': user.get('full_name'),
                'id': user.get('pk'),
                'biography': user.get('biography'),
                'external_url': user.get('external_url'),
                'is_private': user.get('is_private'),
                'is_verified': user.get('is_verified'),
                'is_business': user.get('is_business'),
                'business_category': user.get('category'),
                'can_direct_message': user.get('direct_messaging') if user.get('is_business') else None,
                'email': user.get('public_email') if user.get('is_business') else None,
                'phone_number': f"{user.get('public_phone_country_code')} {user.get('public_phone_number')}" if user.get(
                    'is_business') else None,
                'bio_links': [link.get('url') for link in self.safe_get(user, 'bio_links', [])],
                'total_posts': user.get('media_count'),
                'followers': user.get('follower_count'),
                'following': user.get('following_count'),
                'chaining_suggestions': [
                    {'username': chain.get('username'), 'full_name': chain.get('full_name'), 'pk': chain.get('pk')} for
                    chain in user.get('chaining_suggestions', [])],
                'media_count': user.get('media_count'),
                'total_igtv_videos': user.get('total_igtv_videos'),
                'profile_pic_url': self.safe_get(user, 'hd_profile_pic_url_info.url'),
                'profile_url': f"https://www.instagram.com/{user.get('username')}",
            }
        except Exception as e:
            printer.error(f"Error: {e}")
