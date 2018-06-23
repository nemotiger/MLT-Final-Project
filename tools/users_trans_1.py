'''
output:
1. uid: user id
2. country_lat: latitude of country (inherit from lat_none if unknown)
3. country_lng: longitude of country (inherit from lng_none if unknown)
4. age: age (validated by some reasonable range criteria)
5. privacy_loc: 0=>"country is completely recognizable", 1=>"country can be guessed correctly with high probability", 2=>"country is unavailable or ambiguous"
6. privacy_age: 0=>"age is reasonable", 1=>"age is unreasonable or unavailable"
'''

import sys
import csv
import googlemaps as gm


'''
placeholder latitude and longitude values for unknown places
'''
lat_none = -90.0
lng_none = 0.0

'''
age placeholder for unreasonable or unavailable age
'''
age_none = 0.0 

'''
country_cache:
'country (Case Insensitive)' : (latitude, longitude)
'country long name (Case Insensitive)' : (latitude, longitude)
'country short name (Case Insensitive)' : (latitude, longitude)
'''
country_cache = {}


class GoogleMapsService(object):

    def __init__(self, keyfile):
        self.clients = GoogleMapsService.gmClient(keyfile)
        self.key_count, self.keyfile, self.client = next(self.clients)

    def geocode(self, address):
        while True:
            try:
                return self.client.geocode(address)
            except gm.exceptions.Timeout:
                self.key_count, self.keyfile, self.client = next(self.clients)

    @staticmethod
    def gmClient(keyfile):
        '''
        Create googlemaps.Client with keys in keyfile
        Ask for new key file when running out of keys
        return (#key, keyfile, client)
        '''
        while True:
            try:
                with open(keyfile, 'r') as api_keyfile:
                    for count, key in enumerate(api_keyfile, start=1):
                        try:
                            yield count, keyfile, gm.Client(key=key.strip())
                        except ValueError as err:
                            print(err)
            except FileNotFoundError as err:
                print(err)

            keyfile = input('Enter new GoogleMaps API Key file: ')



def age_trans(age):
    '''
    type(age): string
    return (age, privacy_age)
    '''
    if age == '':
        return age_none, 1.0
    
    age = float(age)
    if age >= 6 and age <= 80:
        return age, 0.0
    else:
        return age_none, 1.0


def init_guess(location):
    '''
    type(location): string
    return (locality, admin1, country, full)
    '''
    location = [ loc.strip() for loc in location.split(',') ]
    if len(location) == 1:
        locality = admin1 = ''
        country = location[0]
    elif len(location) == 2:
        locality = ''
        admin1, country = location
    elif len(location) == 3:
        locality, admin1, country = location
    else:
        locality = location[0:-2]
        admin1 = location[-2]
        country = location[-1]

    full = ','.join(location).strip(',')
    return locality, admin1, country, full



def get_loc(location):
    loc = location['geometry']['location']
    return loc['lat'], loc['lng']


def country_location(gm_service, country):
    '''
    gm_service: GoogleMapsService object
    return country location (lat, lng) or None
    '''
    if country == '':
        return None

    loc = country_cache.get(country.lower())
    if loc is None:
        result = gm_service.geocode(country)
        if len(result) != 1 or 'country' not in result[0]['types']:
            return None
        else:
            loc = get_loc(result[0])
            country_long_name = result[0]['address_components'][-1]['long_name'].lower()
            country_short_name = result[0]['address_components'][-1]['short_name'].lower()
            
            country_cache[country] = loc
            country_cache[country_long_name] = loc
            country_cache[country_short_name] = loc

            return loc
    else:
        return loc


def guess_country(gm_service, location):
    '''
    gm_service: GoogleMapsService object
    return country long name or empty string
    '''
    if location == '':
        return ''
    
    result = gm_service.geocode(location)
    countries = { r['address_components'][-1]['long_name'] for r in result }
    if len(countries) == 1:
        return countries.pop()
    else:
        return ''




if __name__ == "__main__":

    if len(sys.argv) == 4:
        input_csv = sys.argv[1]
        output_csv = sys.argv[2]
        key_file = sys.argv[3]
    else:
        print('Usage: {} <input csv> <output csv> <api key file>'.format(sys.argv[0]))

    gmaps = GoogleMapsService(key_file)

    with open(input_csv, 'r', newline='') as users_csv, \
        open(output_csv, 'w', newline='') as result_csv:

        users_reader = csv.reader(users_csv)
        result_writer = csv.writer(result_csv, quoting=csv.QUOTE_MINIMAL)

        # remove header
        next(users_reader)

        # write header
        result_writer.writerow(['User-ID', 'Country-lat', 'Country-lng', 'Age', 'Privacy-Location', 'Privacy-Age'])

        count = 0
        for uid, location, age in users_reader:

            #Set initial guess value of country and full.
            _, _, country, full = init_guess(location)
            
            # Get country location (lat, lng)
            # Set privacy_loc
            country_loc = country_location(gmaps, country)
            privacy_loc = 0.0
            if country_loc is None:
                country_loc = country_location(gmaps, guess_country(gmaps, full))
                privacy_loc = 2.0 if country_loc is None else 1.0

            lat, lng = country_loc if country_loc is not None else (lat_none, lng_none)

            # Get age, privacy_age
            age, privacy_age = age_trans(age)

            result_writer.writerow([uid, lat, lng, age, privacy_loc, privacy_age])

            count += 1
            if count % 100 == 0:
                print(count)
            
        
        
        
          