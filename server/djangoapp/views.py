from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .restapis import *
from .models import CarModel 

# User registration : 
def user_registration ( request ) : 
    # if method is GET , return the registration form : 
    if request.method == 'GET' : 
        return render ( request , 'registration.html' ) 
    
    # else if method is POST , handle user registration : 
    elif request.method == 'POST' : 
        # get the request data : 
        username = request.POST.get ( 'username' )
        password = request.POST.get ( 'password' )

        # check data is valid : 
        if username=="" or password=="" : 
            messages.warning ( request , 'Invalid username or password data' ) 
            return redirect ( 'registration' )

        # check if user exists : 
        found_user = False 
        try : 
            User.objects.get ( username=username )
            found_user = True 
        except :
            pass
        
        # if user not found , create the user : 
        if not found_user : 
            user = User.objects.create ( username = username , password = password ) 
            # login the user : 
            login ( request , user ) 
            # redirect the user to the home page : 
            return redirect ( 'home' ) 
        
        # else , user exists : 
        # render the registration form with user exist info : 
        else : 
            messages.warning ( request , 'Username already taken, please try a different one' ) 
            return redirect ( 'registration' )

# Login : 
def user_login ( request ) : 
    
    # ensure the request method is POST : 
    if ( request.method == 'POST' ) : 
        # retrieve the request body : 
        username = request.POST.get( 'username' ) 
        password = request.POST.get ( 'password' ) 
        
        # try to authenticate the user : 
        user = authenticate (request , username = username , password = password )  

        # if user has been authenticated : 
        # login user : 
        # redirect to the home page : 
        if user is not None : 
            login ( request , user ) 
            return redirect ( 'home' ) 


        # if user is not authenticated
        # return to the login page again :
        # display the user message : 
        else : 
            messages.warning ( request , "Invalid username or password !")
            return redirect ( 'home' ) 

# Logout : 
def user_logout ( request ) : 
    # logout the user : 
    logout ( request ) 
    # redirect back to home page : 
    return redirect ( 'home' ) 

# About Us  : 
def about_us ( request  ) :
    return render ( request , 'about_us.html'  )


# Contact Us : 
def contact_us ( request ) :
    return render ( request , 'contact_us.html' )

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    # initialize the context : 
    context = {}
    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # update context : 
        context ['dealerships'] = dealerships
        return render ( request , 'index.html',  context )


# get Dealer details , returns the reviews for a dealer : 
def get_dealer_details ( request , dealer_id ) : 

    # backend url : 
    url = 'http://localhost:5000/api/get_reviews'
    # call the get_dealer_reviews_from_cf method : 
    dealer_details = get_dealer_reviews_from_cf ( url , dealer_id=dealer_id )
    print ( dealer_details)
    context= {}
    context['reviews'] = dealer_details 
    context ['dealer_id']= dealer_id

    # return the dealer details view : 
    return render ( request , 'dealer_details.html' , context )

# add a review for a dealership : 
def add_review(request, dealer_id):
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "http://localhost:3000/dealerships/get"
        print ( dealer_id )
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[ dealer_id -1 ].full_name,
            "cars": CarModel.objects.all()
        }
        #print(context)
        return render(request, 'add_review.html', context)
    
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request("http://localhost:5000/api/post_review", review, dealerId=dealer_id)
            print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)