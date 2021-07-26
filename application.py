from flask import Flask, render_template, url_for
from bs4 import BeautifulSoup
import requests
from flask_restful import Api, Resource
from requests.api import get
from settings import *
from model import *
from random import randint

app = Flask(__name__)
# app.config['SECRET_KEY'] = 23 * randint(0, 1000000000000000000)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
db.init_app(app)


class Events(Resource):
    
    def get(self):

        url = "https://www.ufc.com/events"
        locale_cookie = {"STYXKEY_region": "WORLD.en.Europe/Amsterdam"}
        source = requests.get(url, cookies=locale_cookie).text

        soup = BeautifulSoup(source, 'lxml')

        upcoming_event_bg = soup.find("img", {"class": "c-hero__image"})["src"]
        upcoming_events = soup.find("details", {"id": "events-list-upcoming"})
        upcoming_event_data = [[{"Next_event_image": upcoming_event_bg}],[]]

        event_links = upcoming_events.find_all(
            "div", {"class": "c-card-event--result__logo"})
        links = []

        for link in event_links:

            links.append("https://www.ufc.com" + link.find("a", href=True)['href'])

        for link in links:

            event_source = requests.get(link, cookies=locale_cookie).text
            get_event_data = BeautifulSoup(event_source, 'lxml')

            event_name = get_event_data.find(
                "div", {
                    "class":
                    "field field--name-node-title field--type-ds field--label-hidden field__item"
                }).text.strip()
            event_image = get_event_data.find("img", {"class": "c-hero__image"})
            event_date = get_event_data.find(
                "div", {"class": "c-hero__headline-suffix tz-change-inner"})
            event_location = get_event_data.find(
                "div", {
                    "class":
                    "field field--name-venue field--type-entity-reference field--label-hidden field__item"
                })
            main_events = get_event_data.find("details",
                                            {"id": "edit-group-main-card"})
            prelims_events = get_event_data.find("details",
                                                {"id": "edit-group-prelims"})

            early_prelims_events = get_event_data.find(
                "details", {"id": "edit-group-early-prelims"})

            if event_image:
                event_image = event_image['src']
            else:
                event_image = ' '

            if event_date:
                event_date = event_date.text.strip()
            else:
                event_date = ' '

            if event_location:
                event_location = event_location.text.strip()
            else:
                event_location = ' '

            if main_events:

                main_event_fights = main_events.find_all(
                    "div", {"class": "c-listing-fight__content"})
                main_fighters_name = []
                main_weight_class = []
                main_red_corner_img = []
                main_blue_corner_img = []

                for fight in main_event_fights:

                    red_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--red"})
                    main_red_corner_img.append(red_img.find("img")['src'])

                    blue_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--blue"})
                    main_blue_corner_img.append(blue_img.find("img")['src'])

                    name = fight.find_all(
                        "div", {"class": "c-listing-fight__detail-corner-name"})
                    main_fighters_name.append(
                        [name[0].text.strip(), name[1].text.strip()])

                    fight_class = fight.find("div",
                                            {"class": "c-listing-fight__class"})
                    main_weight_class.append(fight_class.text.strip())

            if prelims_events:

                prelims_fighters_name = []
                prelims_weight_class = []
                prelims_red_corner_img = []
                prelims_blue_corner_img = []

                prelims_event_fights = prelims_events.find_all(
                    "div", {"class": "c-listing-fight__content"})

                for fight in prelims_event_fights:

                    red_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--red"})
                    prelims_red_corner_img.append(red_img.find("img")['src'])

                    blue_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--blue"})
                    prelims_blue_corner_img.append(blue_img.find("img")['src'])

                    name = fight.find_all(
                        "div", {"class": "c-listing-fight__detail-corner-name"})
                    prelims_fighters_name.append(
                        [name[0].text.strip(), name[1].text.strip()])

                    fight_class = fight.find("div",
                                            {"class": "c-listing-fight__class"})
                    prelims_weight_class.append(fight_class.text.strip())

            if early_prelims_events:

                early_prelims_fighters_name = []
                early_prelims_weight_class = []
                early_prelims_red_corner_img = []
                early_prelims_blue_corner_img = []

                early_prelims_event_fights = early_prelims_events.find_all(
                    "div", {"class": "c-listing-fight__content"})

                for fight in early_prelims_event_fights:

                    red_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--red"})
                    early_prelims_red_corner_img.append(red_img.find("img")['src'])

                    blue_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--blue"})
                    early_prelims_blue_corner_img.append(
                        blue_img.find("img")['src'])

                    name = fight.find_all(
                        "div", {"class": "c-listing-fight__detail-corner-name"})
                    early_prelims_fighters_name.append(
                        [name[0].text.strip(), name[1].text.strip()])

                    fight_class = fight.find("div",
                                            {"class": "c-listing-fight__class"})
                    early_prelims_weight_class.append(fight_class.text.strip())

            main_event_fighter_images = []
            prelim_event_fighter_images = []
            early_prelim_event_fighter_images = []

            for i in range(len(main_red_corner_img)):

                for j in range(1):

                    main_event_fighter_images.append(
                        [main_red_corner_img[i], main_blue_corner_img[i]])

            for i in range(len(prelims_red_corner_img)):

                for j in range(1):

                    prelim_event_fighter_images.append(
                        [prelims_red_corner_img[i], prelims_blue_corner_img[i]])

            for i in range(len(early_prelims_red_corner_img)):

                for j in range(1):

                    early_prelim_event_fighter_images.append([
                        early_prelims_red_corner_img[i],
                        early_prelims_blue_corner_img[i]
                    ])

            event_data = {
                "Event_name": event_name,
                "Event_location": event_location,
                "Event_date": event_date,
                "Event_image": event_image,
                "Main_event": {
                    "Fighters_name": main_fighters_name,
                    "Fighters_image": main_event_fighter_images,
                    "Weight_class": main_weight_class
                },
                "Prelim_event": {
                    "Fighters_name": prelims_fighters_name,
                    "Fighters_image": prelim_event_fighter_images,
                    "Weight_class": prelims_weight_class
                },
                "Early_prelim_event": {
                    "Fighters_name": early_prelims_fighters_name,
                    "Fighters_image": early_prelim_event_fighter_images,
                    "Weight_class": early_prelims_weight_class
                }
            }

            upcoming_event_data[1].append(event_data)

        return upcoming_event_data

class Stream(Resource):

    def get(self):
        
        url = "https://sportsbay.org/competition/ufc"
        locale_cookie = {"STYXKEY_region": "WORLD.en.Europe/Amsterdam"}
        source = requests.get(url, cookies=locale_cookie).text

        soup = BeautifulSoup(source, 'lxml')
        
        get_stream_url = soup.find("tr", {"class": "vevent"})
        stream_url = get_stream_url.find_all("td")[-1].find("a")['href']

        get_embed_url = "https://sportsbay.org/embed/"+stream_url[6:-1]
        
        return get_embed_url
        


api.add_resource(Events, '/api/upcoming_events')
api.add_resource(Stream, '/api/upcoming_stream')

if __name__ == "__main__":
    app.run(debug=True)
