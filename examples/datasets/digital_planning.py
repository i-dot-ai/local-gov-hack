import requests

data_url = 'https://www.planning.data.gov.uk/entity/'
def get_entity(id):
    response = requests.get(data_url + str(id) + '.json')
    if response.status_code != 200:
        raise Exception('Entity json not found')
    return response.json()

def get_geojson(id):
    response = requests.get(data_url + str(id) + '.geojson')
    if response.status_code != 200:
        raise Exception('Entity geojson not found')
    return response.json()
