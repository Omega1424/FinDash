# Financial Dashboard
#### Video Demo:  https://youtu.be/HYbPQn01MiE
#### Live Demo: https://share.streamlit.io/omega1424/cs50x-final-project/main/app.py
#### Description:
This project is a web app made using python and the open source python-framework Streamlit.
It is used to help one do two things: Find out information about a company to aid their decision in buying that company's stock, and to keep track of their portfolio by adding transactions through a simple input interface that gives out a graph showing the percentage of each stock in the portfolio.

The project contains 4 python files. 2 of them, 'page1.py' and 'page2.py' contain the code, each for their own purpose(company info and portfolio tracking).
Another one, 'multiapp.py' is a file containing code that helped me connect the 2 pages to create a multi page streamlit app. It is imported as a module in the main app.
'app.py' is the main file that simply connects the 2 webpages using the imported module from multiapp.py, and sets some info about the page such as title and layout.

This was a difficult process for me from start to finish, as I encountered many more errors than I ever did in the cs50 psets, which made me understand how different it is to create your own project and solve a preset problem, and there is no straightforward solution or 'check50' hacks other than searching up errors yourself.
I started this project using Dash which is a python framework created by plotly for creating interactive web applications. It worked in some sense, but the errors were so complex I spent days on some, only to give rise to new ones. The graphs not updating themselves after appending a dataframe, keeping the existing info in a frozen "State", all proved too troublesome for me to keep up. Thus i moved to streamlit, which helped me focus more on my webapp itself and its design and functionality rather than trying so hard just to get it to run.
I could have put all my code in one page, but I decided that would be too messy for the reader since there are 2 different purpouses to the functions, which would not need to 'interact' with each other on the same page. However this too was difficult as Streamlit itself had no in built function to add new pages, so I had to draw inspiration from other people's self created modules to create a multi-page streamlit app.
There were more complex graphs made with plotly at first in this webapp, but they did not respond correctly to the python code as the streamlit graphs did, so I removed them. I plan to add thenm when I get a better understanding of dash after this project.
