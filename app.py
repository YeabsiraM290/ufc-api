from flask import Flask
from bs4 import BeautifulSoup
import requests
from flask_restful import Api, Resource
from settings import *
from flask import jsonify

app = Flask(__name__)
# app.config['SECRET_KEY'] = 23 * randint(0, 1000000000000000000)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
# db.init_app(app)


class Events(Resource):
    
    def get(self):

        url = "https://www.ufc.com/events"
        locale_cookie = {"STYXKEY_region": "WORLD.en.Europe/Amsterdam"}
        source = requests.get(url, cookies=locale_cookie).text

        soup = BeautifulSoup(source, 'lxml')

        upcoming_event_bg = soup.find("div", {"class": "layout__region layout__region--content"})
       
        upcoming_event_bg_url = upcoming_event_bg.find("picture").find("img")['src']

        upcoming_events = soup.find("details", {"id": "events-list-upcoming"})
        upcoming_event_data = [[{"Next_event_image": upcoming_event_bg_url}],[]]

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
            event_bg = get_event_data.find("div", {"class": "layout__region layout__region--content"})
           
            event_image = event_bg.find("picture")
          
            
            event_date = get_event_data.find(
                "div", {"class": "c-hero__headline-suffix tz-change-inner"})
            event_location = get_event_data.find(
                "div", {
                    "class":
                    "field field--name-venue field--type-entity-reference field--label-hidden field__item"
                })
            main_events = get_event_data.find("div",
                                            {"id": "main-card"})
            prelims_events = get_event_data.find("div",
                                                {"id": "prelims-card"})

            early_prelims_events = get_event_data.find(
                "div", {"id": "early-prelims"})

            if event_image:
                event_image =  event_image.find("img")["src"]
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
            
            main_fighters_name = []
            main_weight_class = []
            main_red_corner_img = []
            main_blue_corner_img = []

            prelims_fighters_name = []
            prelims_weight_class = []
            prelims_red_corner_img = []
            prelims_blue_corner_img = []

            early_prelims_fighters_name = []
            early_prelims_weight_class = []
            early_prelims_red_corner_img = []
            early_prelims_blue_corner_img = []
           
            if main_events == None:
                main_events = get_event_data.find("section", {"class" : "l-listing--stacked--full-width"})
               

            if main_events:

                main_event_fights = main_events.find_all(
                    "div", {"class": "c-listing-fight__content"})
       

                for fight in main_event_fights:

                    red_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--red"})
                    main_red_corner_img.append(red_img.find("img")['src'])

                    blue_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--blue"})
                    main_blue_corner_img.append(blue_img.find("img")['src'])

                    name = fight.find(
                        "div", {"class": "c-listing-fight__names-row"})
                    red_corner_name = name.find("div", {"class": "c-listing-fight__corner-name c-listing-fight__corner-name--red"})

                    try:
                        red_corner_given_name = red_corner_name.find("span", {"class", "c-listing-fight__corner-given-name"}).text.strip()
                        red_corner_family_name = red_corner_name.find("span", {"class", "c-listing-fight__corner-family-name"}).text.strip()
                        red_corner_name = red_corner_given_name + " " + red_corner_family_name
                    except:
                        red_corner_name = red_corner_name.text.strip()

                    blue_corner_name = name.find("div", {"class": "c-listing-fight__corner-name c-listing-fight__corner-name--blue"})
                    try:
                        blue_corner_given_name = blue_corner_name.find("span", {"class", "c-listing-fight__corner-given-name"}).text.strip()
                        blue_corner_family_name = blue_corner_name.find("span", {"class", "c-listing-fight__corner-family-name"}).text.strip()
                        blue_corner_name = blue_corner_given_name + " " + blue_corner_family_name
                    except:
                        blue_corner_name = blue_corner_name.text.strip()

                    main_fighters_name.append(
                        [red_corner_name, blue_corner_name ])

                    fight_class = fight.find("div",
                                            {"class": "c-listing-fight__class"})
                    main_weight_class.append(fight_class.text.strip())

            if prelims_events:

                prelims_event_fights = prelims_events.find_all(
                    "div", {"class": "c-listing-fight__content"})

                for fight in prelims_event_fights:

                    red_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--red"})
                        
                    prelims_red_corner_img.append(red_img.find("img")['src'])

                    blue_img = fight.find(
                        "div", {"class": "c-listing-fight__corner-image--blue"})
                    prelims_blue_corner_img.append(blue_img.find("img")['src'])

                    name = fight.find(
                        "div", {"class": "details-content__header"})

                    prelims_red_corner_name = name.find("div", {"class": "details-content__name details-content__name--red"})

                    try:
                        prelims_red_corner_given_name = prelims_red_corner_name.find("span", {"class", "details-content__corner-given-name"}).text.strip()
                        prelims_red_corner_family_name = prelims_red_corner_name.find("span", {"class", "details-content__corner-family-name"}).text.strip()
                        prelims_red_corner_name = prelims_red_corner_given_name + " " + prelims_red_corner_family_name
                    except:
                        prelims_red_corner_name = prelims_red_corner_name.text.strip()

                    prelims_blue_corner_name = name.find("div", {"class": "details-content__name details-content__name--blue"})
                  

                    try:
                        prelims_blue_corner_given_name = prelims_blue_corner_name.find("span", {"class", "details-content__corner-given-name"}).text.strip()
                        prelims_blue_corner_family_name = prelims_blue_corner_name.find("span", {"class", "details-content__corner-family-name"}).text.strip()
                        prelims_blue_corner_name = prelims_blue_corner_given_name + " " + prelims_blue_corner_family_name
                    except:
                 
                        prelims_blue_corner_name = prelims_blue_corner_name.text.strip()
                        

                    prelims_fighters_name.append(
                        [prelims_red_corner_name,  prelims_blue_corner_name])

                    fight_class = fight.find("div",
                                            {"class": "details-content__class"})
                    prelims_weight_class.append(fight_class.text.strip())

            if early_prelims_events:



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

                    name = fight.find(
                        "div", {"class": "c-listing-fight__names-row"})

                    early_prelims_red_corner_name = name.find("div", {"class": "c-listing-fight__corner-name c-listing-fight__corner-name--red"})

                    try:
                        early_prelims_red_corner_given_name = early_prelims_red_corner_name.find("span", {"class", "c-listing-fight__corner-given-name"}).text.strip()
                        early_prelims_red_corner_family_name = early_prelims_red_corner_name.find("span", {"class", "c-listing-fight__corner-family-name"}).text.strip()
                        early_prelims_red_corner_name= early_prelims_red_corner_given_name + " " + early_prelims_red_corner_family_name
                    except:
                        early_prelims_red_corner_name = early_prelims_red_corner_name.text.strip()

                    early_prelims_blue_corner_name = name.find("div", {"class": "c-listing-fight__corner-name c-listing-fight__corner-name--blue"})
                    try:
                        early_prelims_blue_corner_given_name = early_prelims_blue_corner_name.find("span", {"class", "c-listing-fight__corner-given-name"}).text.strip()
                        early_prelims_blue_corner_family_name = early_prelims_blue_corner_name.find("span", {"class", "c-listing-fight__corner-family-name"}).text.strip()
                        early_prelims_blue_corner_name = early_prelims_blue_corner_given_name + " " + early_prelims_blue_corner_family_name
                    except:
                        early_prelims_blue_corner_name = early_prelims_blue_corner_name.text.strip()

                    early_prelims_fighters_name.append(
                        [early_prelims_red_corner_name, early_prelims_blue_corner_name ])
     

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

        return jsonify(upcoming_event_data)

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
