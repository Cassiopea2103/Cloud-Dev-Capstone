from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
 
    # User registration : 
    path ( route = 'user_register' , view = views.user_registration , name = 'registration' )  ,

    # User login : 
    path ( route = 'user_login' , view = views.user_login , name = 'login' ) ,

    # User Logout : 
    path ( route = 'user_logout' , view = views.user_logout , name = 'logout' ) ,

    # About Us :
    path ( route = 'about' , view = views.about_us , name = "about") ,

    # Contact Us :
    path ( route = 'contact', view = views.contact_us, name="contact" ) ,


    path(route='', view=views.get_dealerships, name="home"),

    # path for dealer reviews 
    path ( route = 'dealer/<int:dealer_id>' , view = views.get_dealer_details , name = 'dealer_details' ),

    # path for add a review view
    path ( route='add_review/<int:dealer_id>' , view = views.add_review , name = 'add_review' ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)