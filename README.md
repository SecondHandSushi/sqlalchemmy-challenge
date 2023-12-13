# sqlalchemy-challenge
Matthew Idle 
Univeresity of Minnesota Data Analytics and Visulaization Bootcamp

App.py
This python app uses the sqlalchemy ORM to interface with a sqlite database, then uses Flask to create an API to interface with that sqlite database. 

Basic operation:
Import dependencies, automap bases, reflect, and save references to both tables, measurement and stations. Landing page was created to show the endpoints.
All are static routes, with the exception of the last two, which are dynamic. The dynamic routes are accessed by entereing dates in the date range and format provided. If the date entered is outside of the given range, or the start date is after the end date, then a message is displayed prompting the user to enter a new date(s). The session is then created, and the tables are queried. A list is used to make things easier to follow when quering more than three variables. The results are then unpacked into dictionaries and jsonified and returned.


references:
1)Hall, Cyan. “Sqlalchemy Cheatsheet.” CyanHall.Com, 2023, www.cyanhall.com/cheatsheet/22.SQLAlchemy-cheatsheet/. 
2)Sheet, Py. “Sqlalchemy - Pysheeet.” SQLAlchemy - Pysheeet, www.pythonsheets.com/notes/python-sqlalchemy.html. Accessed 12 Dec. 2023.
3)Petrou, Theodore. Panda’s Cookbook: Recipes for Scientific Computing, Time Series Analysis and Data Visualization Using Python. first ed., Packt Publishing, 2017. 
