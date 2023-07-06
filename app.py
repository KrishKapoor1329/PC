import csv
from geopy.distance import geodesic
from flask import Flask, render_template, request

app = Flask(__name__)

def load_data_from_csv():
    data = []
    with open('C:/Users/krish/PC/pet_services.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def load_zipcodes():
    zipcodes = {}
    with open('C:/Users/krish/PC/zipcodes.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            zipcode = row['ZIP']
            lat = float(row['LAT'])
            lon = float(row['LON'])
            zipcodes[zipcode] = (lat, lon)
    return zipcodes

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).miles

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        user_zipcode = request.form['zipcode']

        # Load the CSV data
        data = load_data_from_csv()

        # Load the ZIP codes and coordinates
        zipcodes = load_zipcodes()

        # Calculate distances from user zipcode to all zipcodes in the CSV
        distances = []
        if user_zipcode in zipcodes:
            user_coord = zipcodes[user_zipcode]
            for row in data:
                zipcode = row['Zip']
                if zipcode in zipcodes:
                    location_coord = zipcodes[zipcode]
                    distance = calculate_distance(user_coord, location_coord)
                    distances.append({
                        'Name of Location': row['Name of Location'],
                        'Address': row['Address of Location'],
                        'City': row['City'],
                        'State': row['State'],
                        'Website': row['Website'],
                        'Phone Number': row['Phone Number'],
                        'Distance': distance
                    })

        # Sort the distances and get the 5 closest locations
        closest_locations = sorted(distances, key=lambda x: x['Distance'])[:5]
        closest_location_names = [location['Name of Location'] for location in closest_locations]

        # Return the result to a template for display
        return render_template('results.html', locations=closest_locations)

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)




from flask import Flask, Response
from gevent.pywsgi import WSGIServer
from gevent import monkey

# need to patch sockets to make requests async
# you may also need to call this before importing other packages that setup ssl
monkey.patch_all()


# define some REST endpoints... 

def main():

    # use gevent WSGI server instead of the Flask
    # instead of 5000, you can define whatever port you want.
    http = WSGIServer(('', 5000), app.wsgi_app) 

    # Serve your application
    http.serve_forever()

if __name__ == '__main__':
    main()

