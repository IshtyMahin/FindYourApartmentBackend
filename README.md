# FindYourApartmentBackend


It is backend server of my FindYourApartment website. It provides user registration,authentication. 

## Features 

  1. User management:

  - Registration: Users can register with their information
  - Users can register as either a normal user or an apartment user.
  - Email Verification: A confirmation email is sent for email verification
  - Login/Logout: Registered users can log in and log out of their accounts.


  2. Apartment management:

  - We can list apartments with details such as price,address, bedrooms, bathrooms,size and other information. 

  - A apartment owner can add a apartment for rent.He also update and delete his added appartment information. 


3. Booking Management:

- Users can book appointments for apartment viewings with select data and time. 

4. Favorite Management:

- Users can add apartments to their favorites list. 
- Users can view their favorite apartment list. 
- Users also remove apartments from their favorites list. 


Technologies Used :

- Django 
- Django REST Framework
- Database: PostgreSQL

Run with:

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver