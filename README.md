# KeywordShortcut
The keyword shortcut microservice for our Group 25 team assignment

This is A WORK IN PROGRESS and is effectively my first time at creating anything in Github

Here are the basics of what we currently envision this microservice to do:

1. Will use Flask to communicate through various main programs using HTTP requests. This way, the programmer's language of choice (C, Java, so on...) will not
   come into issue when running the microservice. This will be running a local server and be ran on keyword_service.py.

   1a. This microservice will use Python, but don't be worried: your main program does not need to be in Python to run the microservice!

         1ab. However, you will need to install Python onto your computer.

   1b. For the Flask server to work, it will have to run locally. There is a way that it can work via someone's own computer acting as the host server, but
       for the scope of this project, we're keeping it local.

         1ba. In order to run the Flask server locally:

               - clone the repository
               - open the cloned repository
               - if you do not have the required installs, open windows terminal and input py -m pip install Flask
               - Flask needs to stay running in order to operate correctly, if the terminal is closed it will
                 stop running.
               - if you would like to manually close the Flask instance, input CTRL + C into the terminal

         1bb. Now that you have Flask installed and whatnot, we will move onto actually running the microservice
                - in the repository's main directory, run py -m flask --app keyword_service run

         1bc. IMPORTANT: as of 10/29/2026, the address created in your terminal will direct you to a webpage that
                         just says "Keyword Microservice is running!" or something along those lines, this will
                         be changed to where it will actually operate as intended.

                1bd. Additionally, the Flask file does nothing but ensure that the service works as intended, which
                      at this point it does. 
   

2. keyword_search is the meat and potatoes of the program. It will include the search function itself, as well as the library of words each
   keyword will be associated with. We will start small, and build on as time goes.


