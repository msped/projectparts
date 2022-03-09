# Project Parts

Before reading any further please be aware this site is using stripe.js to take payments. In order for it to work please use the credit card number `4242424242424242` (`4242` four times). If you use your own details a <strong><u>payment maybe taken.</u></strong>

Project Parts is an online competition to win car modifactions parts, it can be views [here](https://projectparts.herokuapp.com/).

[![Build Status](https://travis-ci.org/msped/projectparts.svg?branch=master)](https://travis-ci.org/msped/projectparts)

## UX

Project parts is a competition website for car enthusiasts who wish to play for the more expensive car modification parts. The target audience is the car modification community.

The site will offer 'tickets' at a fraction of the cost of the full product price. Each competition will have a set amount of tickets before the competition ends and a winner is drawn randomly. All enterants must get the question correct in-order to be entered into a competition.

- A User will want to create a profile so that they can see previously entered competitions and there winner.

- A User will want to search on modifications by either categories or the car model they fit.

- A User will want a payment system in-order to pay for the tickets they wish to play.

- A User will want to search through previous orders.

- A User will want to be able to see the price of the full product as if they were to buy it compared to the ticket price.

- A User will want to be able to quick add set amount of tickets with the option to add a specific amount when viewing a product in more detail.

- Users will want to be able to read more about each product on there own page with more description.

- User will want a cart that tickets can be added to and updated with the amount. A cart will display the ticket price, quantity and the full total.

### Wireframes

Wireframes for the site can be viewed [here](https://github.com/msped/projectparts/tree/master/assets/wireframes/exports)

### Database Design

Design of the database can be viewed [here](https://github.com/msped/projectparts/blob/master/assets/wireframes/Project%20Parts%20ERD.png)

## Features

### Existing Features

- All products are shown, 15 per page, unless a user search for specific vehicle.

- When orders have been made they are viewable in the users profile.

- Profile details are editable within a users profile. If a profile is incomplete a check engine light will display next to the users first name on the navbar.

- Each carts item is automatically assigned an entry to number to the competition if the user answer the competitions question correctly.

- New competition is automatically created when active competition is below a certain number of entries.

- Competition automatically ends, picks a winner and announces the winner via e-mail before starting the next competition.

- All previous winners are viewable on the winners page with associated question, answer, ticket number and product won.

- When a user enters a competition they will receive an e-mail with the order and entries if the user got the answer correct.

### Features Left to Implement

More ideas I would like to implement on the site are:

- Promotional e-mails with new or discounted products.

- Add a vehicle API and/or bridge table for better search functionality.

- To add a bundle feature for multiple products with a discount based on amount of products in a bundle.

- Discount Codes at checkout.

## Technologies Used

Below are the techbologies used with this project.

- [HTML](https://en.wikipedia.org/wiki/HTML)

- [CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)

- [jQuery](https://jquery.com/)

- [Django](https://www.djangoproject.com/)
  - [Django Forms Boostrap](https://pypi.org/project/django-forms-bootstrap/)

- [Font Awesome](https://fontawesome.com/)

- [Pillow](https://python-imaging.github.io/)

- [Stripe](https://stripe.com/gb)

- [PostgreSQL](https://www.postgresql.org/)

## Testing

Forms, URLs and models for each application with the project have been test using automated tests. You can run these tests with `python manage.py test` or if you wish to run a specific applications test type `python manage.py test *application_name*`.

[HTML](https://validator.w3.org/) & [CSS](http://jigsaw.w3.org/css-validator/) was validated with W3C validation service. Javascript was validated with [jshint](https://jshint.com/).

Each page was tested on a screen size from desktop down to iPhone 5 (320x568). An issue will only arise if a user has a phone will with smaller screen resolution which shouldn't be an issue when Apple users using an iPhone 4 - iPhone 5S is 1.43%, smaller screens will cause an issue where tables are in use to display data like in the user orders page.

## Deployment

### Locally

In order to run the code locally you must first clone this repository, `git clone https://github.com/msped/projectparts.git`. Once cloned setup a virtual environment by first using `python -m venv *venv name*`. To access the venv you need to start the venv, for exmaple in my case `projectparts-env\scripts\activate.bat`. Once the venv has been started you can then install the packages using `pip intsall -r requirements.txt`. You run the code locally by running `python manage.py runserver` and go to `http://127.0.0.1:8000/` to see the development site on your local machine.

In order for the site to work either locally or on heroku they will need the env / config variables outlined below.

### Heroku

In order to deploy to heroku I created a new app within Heroku on called projectparts choosing a region that I was in. For this project to work on Heroku it requires 'Heroku Postgres' and 'SendGrid' under resources / add-ons.

Once the add-ons are up and running under the deploy tab I choose GitHub and connected to my repository. I chose to enable automatic deploys so that the site will update after each push to master. Below this section deploy the project from the master branch and wait for the build to complete.

You can see the project hosted [here](https://projectparts.herokuapp.com/).

### .env / Config Vars

SECRET_KEY - Random secret key</br>
STRIPE_PUBLISHABLE - Pushlishable key provided by stripe.js</br>
STRIPE_SECRET - Secret Key provided by stripe.js</br>
AWS_ACCESS_KEY_ID - Amazon Web Services Access for using S3 Bucket</br>
AWS_SECRET_ACCESS_KEY - Amazon Web Services Secret key.</br>

For local deployment you will need to use your own e-mail account to send e-mails:</br>
EMAIL_ADDRESS - This will be the email address you will be using to send emails from, in my case a gmail account.</br>
EMAIL_PASSWORD - The password associated with the above.</br>

On Heroku the sending of e-mail will be handled with the SendGrid add-on:</br>
SENDGRID_USERNAME - Provided by SendGrid API</br>
SENDGRID_PASSWORD - Provided by SendGrid API</br>

## Credits

### Content / Media

The jumbotron image on the homepage was obtain from [here](https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwisoejaoZDnAhVB1BoKHQEIDHwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.rias.co.uk%2Fnews-and-guides%2Fdemystifying-insurance%2Fdo-car-modifications-affect-car-insurance-premiums%2F&psig=AOvVaw0ARVj92T-jmSWrHYQHcJ-q&ust=1579543813621550).

Loading gif was obtained from [here](https://www.estabulo.co.uk/wp-content/plugins/interactive-3d-flipbook-powered-physics-engine/assets/images/dark-loader.gif)

The check engine light used in the incompletion of a users profile is from [here](https://en.wikipedia.org/wiki/Check_engine_light#/media/File:Motorkontrollleuchte.svg).

All other text and images where taken from the corresponding site that is on the product detail page, linked at the bottom.
