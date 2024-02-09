from django.shortcuts import render
from django.shortcuts import  render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 

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
    context = {}
    if request.method == "GET":
        return render(request, 'index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

