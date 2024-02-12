import requests
from requests.auth import HTTPBasicAuth
import json
from .models import CarDealer , DealerReview 


# get_request : 
def get_request ( url , **kwargs ) : 
    
    try : 
        # get response :
            # if api key is provided : 
            if 'api_key' in kwargs : 
                response = requests.get ( url , headers = {'Content-Type': 'application/json' } , params = kwargs , auth=HTTPBasicAuth('apikey', kwargs ['api_key'])) 
            else : 
                 response = requests.get ( url , headers = {'Content-Type': 'application/json' } , params = kwargs  )
    except : 
        print ( 'Network exception occurred' ) 
    
    
    status_code = response.status_code 
    print ( 'With status {}'.format ( status_code ) ) 

    json_data = json.loads ( response.text ) 
    return json_data 

# post request : 
def post_request ( url , json_payload , **kwargs ) : 
    print(f"POST {url}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    
    json_data = json.loads(response.text)
    return json_data



# get dealerss : 
def get_dealers_from_cf ( url , **kwargs ) : 
    # prepare the result array : 
    results = []

    # get response data : 
    json_result = get_request( url )

    if json_result : 
        # for each dealer object :
        # get the row list as dealers : 
        dealers = json_result 
        for dealer in dealers : 
            # get its content in 'doc' object : 
            # instanciate a CarDealer object : 
            car_dealer = CarDealer ( id = dealer["id"] , city = dealer["city"] , state=dealer["state"] , st=dealer["st"], address=dealer["address"],zip=dealer["zip"], lat=dealer["zip"] , short_name=dealer["short_name"] , full_name=dealer["full_name"], long=dealer["long"])

            # append the car dealer object : 
            results.append ( car_dealer )

        return results


def get_dealer_by_id ( url , dealer_id ) : 

    # call the get_request function : 
    response = get_request ( url , id = dealer_id )
    # if we got a json result : 
    if response : 
        car_dealer = CarDealer ( id = response['id'] , city=response['city'] , state = response['state'] , st = response['st'], address=response['address'] , zip = response['zip'], lat=response['lat'], long=response['long'], short_name=response['short_name'] , full_name=response['full_name'] )

        return car_dealer


# get dealer by state : 
def get_dealer_by_state ( url , state ) : 

    # call the get_request function : 
    response = get_request ( url , state=state ) 
    
    # if we got a json result : 
    if response : 
        car_dealer = CarDealer ( id = response['id'] , city=response['city'] , state = response['state'] , st = response['st'], address=response['address'] , zip = response['zip'], lat=response['lat'], long=response['long'], short_name=response['short_name'] , full_name=response['full_name'] )

        return car_dealer
         
# get dealer reviews : 
def get_dealer_reviews_from_cf ( url , dealer_id ) :
    # initialize the results array : 
    results = []
    # call the get request function : 
    response = get_request ( url , id = dealer_id )  
    print ( response )   

    # if response : 
    # iterate through the response reviews : 
    if response : 
        for review in response : 
            # create a dealer review object : 
            dealer_review = DealerReview ( id = review['id'] , name = review['name'] , dealership=review['dealership'], review=review['review'], purchase=review['purchase'] , purchase_date=review['purchase_date'], car_make=review['car_make'] , car_model=review['car_model'] , car_year=review['car_year'] , sentiment = analyze_review_sentiments( review['review']))

            # append the review to the results array : 
            results.append ( dealer_review ) 
    
    # return the results : 
    return results 


# sentiment analysis WATSON:  
def analyze_review_sentiments(text):
    URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/0fcb999e-e3db-4074-a34e-a97275e5ec06'
    API_KEY = 'mSoDtTjwKmzJsj_z47QZdz4TCXHSpuPo-PrJ16V5o9UI'
    params = json.dumps({"text": text, "features": {"sentiment": {}}})
    response = requests.post(
        URL, data=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', API_KEY)
    )
    try:
        return response.json()['sentiment']['document']['label']
    except KeyError:
        return 'neutral'