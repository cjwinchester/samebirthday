#samebirthday

A Python 3.6+ script that, handed _your birthday_ (or any date, whatever) in `YYYY-MM-DD` format, grabs the "#Birth" list from the Wikipedia page for that specific day ([like this one](https://en.wikipedia.org/wiki/July_12#Births)) and prints out all of the Wikipedia-famous people who share your birthday.

I'm using `pipenv` to manage the two dependencies (`requests` and `bs4`), but use whatever makes you happiest.

Sample usage, assuming you're in your virtual environment: `python samebday.py "1945-07-12"`.

Redirect to a text file: `python samebday.py "1945-07-12" > my_birthday_buds.txt`