from django.db import models

#Car Make :
class CarMake ( models.Model ) : 
    name = models.CharField ( max_length = 50 , null = True ) 
    description = models.TextField (null = True )

    def __str__ ( self ) : 
        return self.name 

# Car : 
class CarModel ( models.Model ) : 
    car_make = models.ForeignKey ( CarMake , on_delete = models.CASCADE , null = True ) 
    name = models.CharField ( max_length = 50 , null = True ) 
    dealer_id = models.IntegerField () 
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Coupe', 'Coupe'),
        ('Convertible', 'Convertible'),
        ('Hatchback', 'Hatchback'),
        ('Wagon', 'Wagon'),
        ('Pickup Truck', 'Pickup Truck'),
    ]
    model_type = models.CharField ( max_length = 12 , choices =  CAR_TYPES ) 
    year = models.DateField ( ) 
    def __str__ ( self ) : 
        return self.name 

class CarDealer :
    def __init__ ( self , id , city , state , st , address , zip , lat , long , short_name , full_name ) :
        self.id = id 
        self.city = city 
        self.state = state 
        self.st = st 
        self.address = address 
        self.zip = zip 
        self.lat = lat 
        self.long = long 
        self.short_name = short_name 
        self.full_name = full_name

    def __str__ ( self ) : 
        return "Dealer name : " + self.full_name

class DealerReview : 
    def __init__ ( self , id , name , dealership , review , purchase , purchase_date , car_make , car_model , car_year , sentiment  ) : 
        self.id = id 
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment 

    def __str__ ( self ) :
        return "Reviewer : " + self.name + " Review :  " + self.review  + " Sentiment : " + self.sentiment + '\n'