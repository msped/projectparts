# Project Parts

Project Parts is an online competition to win car modifactions parts.

[![Build Status](https://travis-ci.org/msped/projectparts.svg?branch=master)](https://travis-ci.org/msped/projectparts)

## UX

Project parts is a competition website for car enthusiasts who wish to play for the more expensive car modification parts. The target audience is the car modification community.

The site will offer 'tickets' at a fraction of the cost of the full product price. Each competition will have a set amount of tickets before the competition ends and an winner is drawn randomly. All enterants must get the question correct in-order to be entered into a competition.

- A User will want to create a profile so that they can see previously entered competitions and there winner.

- A User will want to search on modifications by either categories or the car model they fit.

- A User will want a payment system in-order to pay for the tickets they wish to play.

- A User will want to search through previous orders.

- A User will want to be able to see the price of the full product as if they were to buy it compared to the ticket price.

- A User will want to be able to quick add set amount of tickets.

- Users will want to be able to read more about each product on there own page with more description.

- User will want a cart that tickets can be added to and updated with the amount. A cart will display the ticket price, quantity and the full total.

### Wireframes

Wireframes for the site can be viewed [here](https://github.com/msped/projectparts/tree/master/assets/wireframes/exports)

### Database Design

Design of the database can be viewed [here](https://github.com/msped/projectparts/blob/master/assets/wireframes/Project%20Parts%20ERD.png)

## Features

### Existing Features

Feature 1 - allows users X to achieve Y, by having them fill out Z

- Products page displays 15 products as a standard, showing full products when using search filters.

- When orders have been made they are viewable in the users profile.

- Profile details are editable within a users profile. If a profile is incomplete a check engine light will display next to the users first name on the navbar.

- Each carts item is automatically assigned an entry to number to the competition.

- New competition is automatically created when active competition is below a certain number of entries.

- Competition automatically ends, picks a winner and announces the winner via e-mail before starting the next competition.

- All previous winners are viewable on the winners page with associated question, answer, ticket number and product won.

- When a user enters a competition they will receive an e-mail with the order and entries if the user got the answer correct.

### Features Left to Implement

More ideas I would like to implement on the site are:

- Promotional e-mails with new or discounted products.

- Add a vehicle API for better vehicle search functionality.

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

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Forms, URLs and models for each application with the project have been test using automated tests. You can run these tests with `python manage.py test` or if you wish to run a specific applications test type `python manage.py test *application_name*`.

*NON AUTOMATED TESTS*

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:

Different values for environment variables (Heroku Config Vars)?
Different configuration files?
Separate git branch?
In addition, if it is not obvious, you should also describe how to run your code locally.

Locally the code is ran using a virutal environment (venv). To access the venv you need to start the venv, for exmaple in my case `projectparts-env\scripts\activate.bat`. Once
the venv has been started you can then run `python manage.py runserver` and go to http://127.0.0.1:8000/ to see the development site on your local machine.

## Credits

### Content / Media

The check engine light used in the incompletion of a users profile is from [here](https://en.wikipedia.org/wiki/Check_engine_light#/media/File:Motorkontrollleuchte.svg).

All other text and images where taken from the corresponding site that is on the product detail page, linked at the bottom.
