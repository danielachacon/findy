class GTLocations:
    
    _locations = {
        "Klaus Advanced Computing Building": {
            "name": "Klaus Advanced Computing Building",
            "latitude": 33.77703198660274,
            "longitude": -84.39581979530878,
        },
        "Tech Tower": {
            "name": "Tech Tower",
            "latitude": 33.772502795117354,
            "longitude":  -84.39469725947366,
        },
        "John Lewis Student Center": {
            "name": "John Lewis Student Center",
            "latitude": 33.77374055939793,
            "longitude": -84.3990191298733,
        },
        "Bobby Dodd Stadium": {
            "name": "Bobby Dodd Stadium",
            "latitude": 33.77258629442485,
            "longitude": -84.39326184101535,
        },
        "Price Gilbert Memorial Library": {
            "name": "Price Gilbert Memorial Library",
            "latitude": 33.774362709511806,
            "longitude": -84.39564742470908,
        },

        "Crosland Tower": {
            "name": "Crosland Tower",
            "latitude": 33.774089201734796,
            "longitude": -84.39503348714562,
        },

        "Campus Recreation Center": {
            "name": "Campus Recreation Center",
            "latitude": 33.77554018902857,
            "longitude":  -84.4035657077155,
        },
        "Kendeda Building": {
            "name": "Kendeda Building for Innovative Sustainable Design",
            "latitude": 33.77860391340361,
            "longitude": -84.39957016278323,
        },
        "Clough Undergraduate Learning Commons": {
            "name": "Clough Undergraduate Learning Commons",
            "latitude": 33.77488398521875,
            "longitude": -84.39640715742608,
        },
        "Ferst Center for the Arts": {
            "name": "Ferst Center for the Arts",
            "latitude": 33.775119227614816,
            "longitude": -84.39926054505653,
        },
        "North Avenue Dining Hall": {
            "name": "North Avenue Dining Hall",
            "latitude": 33.77104799347537,
            "longitude": -84.3914564642262,
        },
        "Kessler Campanile": {
            "name": "Kessler Campanile",
            "latitude": 33.7743090219788,
            "longitude": -84.39817469853617
        },
        "McCamish Pavilion": {
            "name": "McCamish Pavilion",
            "latitude": 33.78078642077381,
            "longitude":  -84.39281951905559,
        },
        "Tech Green": {
            "name": "Tech Green",
            "latitude": 33.77457488878495,
            "longitude": -84.3973376811334,
        },
        "Paul G. Mayer Memorial Gardens": {
            "name": "Paul G. Mayer Memorial Gardens",
            "latitude": 33.77360198005765,
            "longitude": -84.39564587336201,
        }
    }
    
    @classmethod
    def get_location(cls, name):
        return cls._locations.get(name)
    
    @classmethod
    def get_all_locations(cls):
        return list(cls._locations.values())

    @classmethod
    def get_location_names(cls):
        return list(cls._locations.keys()) 