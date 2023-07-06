import csv
from geopy.geocoders import Nominatim

def get_coordinates(zipcodes):
    geolocator = Nominatim(user_agent="zipcode_locator")
    coordinates = []
    for zipcode in zipcodes:
        location = geolocator.geocode(zipcode)
        if location:
            lat = location.latitude
            lon = location.longitude
            coordinates.append({'ZIP': zipcode, 'LAT': lat, 'LON': lon})
    return coordinates

def save_coordinates_to_csv(coordinates, filename):
    fieldnames = ['ZIP', 'LAT', 'LON']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(coordinates)

# Example usage
zipcodes = [
    '60618', '60618', '60607', '60616', '60616', '60622', '60612', '60612', '60647', '60607',
    '60660', '60544', '60647', '60423', '60202', '60174', '60516', '60061', '60051', '60067',
    '60056', '60140', '60504', '60195', '60025', '60560', '60140', '60174', '60061', '60067',
    '60051', '60516', '60195', '60056', '60504', '60560', '60504', '60544', '60423', '60174',
    '60516', '60560', '10010', '10010', '10012', '10001', '11216', '7755', '11109', '10025',
    '11101', '10023', '11105', '7029', '10019', '7302', '8510', '90034', '90232', '90025',
    '90015', '90301', '90048', '90025', '91352', '90025', '90248', '90064', '91105', '90046',
    '91502', '91502', '91335', '91423', '91605', '90015', '91604', '91204', '90290', '92507',
    '92807', '91504', '91423', '92614', '90046', '92627', '91356', '91030', '90505', '90254',
    '91741', '90405', '91101', '90290', '92606', '91343', '92708', '91710', '91604', '92806',
    '92708', '91723', '91390', '92627', '92831', '91710', '92677', '98144', '98291', '98021',
    '98077', '98012', '98072', '98034', '98028', '98188', '98072', '27610', '27560', '27560',
    '27610'
]

coordinates = get_coordinates(zipcodes)
save_coordinates_to_csv(coordinates, 'zipcode_coordinates.csv')
