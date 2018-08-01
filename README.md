## Stuart's Astro page
Thank you for your interest in Stuart's Astro page project. I have a passion for Space so I've chosen to base my project on astronomical objects

## Description
Stuart's Astro page Project page is a web application that was created as a physical manifestation of my learnings in Udacity's Full Stack Developer course 'Part 3 - The Backend'.
The page shows a variety of astronomical categories and the associated items within that category.
Users are able to login with their Google credentials.
Logged in users are able to create new categories and add new items to their categories.
Users are able to edit and delete items & categories which they have created

## Quickstart
If using a virtual Linux machine start the virtual machine. e.g. for Virtual box and Vagrant you can use the following commands
vagrant up
vagrant ssh 
Place the unzipped folder inside a folder accessible to your virtual machine (if using a virtual machine) and CD into the folder
To create the database run python database_setup.py
To populate the database run python lotsofastronomicalobjects.py
To launch the webserver and application run python application.py
To access the web application open a browser and type: http://localhost:5000/astro

## JSON endpoints
Four JSON endpoints are provided. You can access them as follows:
1. A JSON endpoint showing all items: http://localhost:5000/astro/JSON
2. A JSON endpoint showing all categories: http://localhost:5000/astro/catJSON
3. A JSON endpoint showing the items within a category: http://localhost:5000/astro/<category ID goes here>/JSON
4. A JSON endpoint showing a specific item within a category: http://localhost:5000/astro/<category ID goes here>/<item ID goes here>/JSON

## System Requirements
Stuart's Astro page requires:
- Any modern browser capable of displaying HTML files
- An active internet connection
- Python 2.7 https://www.python.org/downloads/
- PSQL
- A linux machine or virtual machine (such as Vagrant with VirtualBox)
	- VirtualBox installation https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
	- Vagrant installation https://www.vagrantup.com/downloads.html
	- The virtual machine configuration I used can be found at:
	https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip

## Additional security
To protect against Cross Site Request Forgery this web application generates an anti-forgery state token

## Note
This project was completed while watching Udacity training videos and following along.
Additionally, CSS, HTML and Python files were provided for an earlier 'restaurant' project which served as the basis for much of the work on this web app.
I therefore do not claim that this website is solely the product of my original thought

## Additional Sources
Login and logout buttons: I found instructions for creating a CSS buttons here https://www.w3schools.com/css/css3_buttons.asp
I made substantial use of official Python documentation (www.python.org), Flask documentation (http://flask.pocoo.org/) stackoverflow.com 
as well as Google and Udacity course work to create this programme