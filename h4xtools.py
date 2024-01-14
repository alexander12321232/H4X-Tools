#!/usr/bin/env python3

"""
 Copyright (c) 2024. Vili and contributors.

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

from flask import Flask, render_template, request
from utils import (
    email_search,
    search_username,
    ig_scrape,
    whois_lookup,
    webhook_spammer,
    port_scanner,
    ip_lookup,
    phonenumber_lookup,
    websearch,
    smsbomber,
    web_scrape,
    wifi_finder,
    wifi_password_getter,
    fake_info_generator,
    dirbuster,
    local_accounts_getter,
    caesar_cipher,
    basexx
)
from helper import printer

app = Flask(__name__)
app.template_folder = "web/templates"
app.static_folder = 'web/static'
VERSION = "dev.1"


@app.route('/')
def index():
    return render_template('index.html', version=VERSION)


@app.route('/ig_scrape')
def ig_scrape_route():
    try:
        username = request.form['username']
        password = request.form['password']
        target = request.form['target']

        scraper = ig_scrape.Scrape(username, password, target)
        result_message = f"IG Scrape for {target} completed successfully."
        scraped_data = scraper.scraped_data

        return render_template('igscrape.html', result_message=result_message, scraped_data=scraped_data)

    except Exception as e:
        error_message = f"Error during IG scrape: {e}"
        return render_template('igscrape.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
