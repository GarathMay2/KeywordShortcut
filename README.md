# KeywordShortcut
The keyword shortcut microservice for our Group 25 team assignment

!! UPDATED AS OF 11/14/26 !!
 - The keyword-search.py file will be removed, as its existence was redundant.
 - Shifted from using Flask to ZeroMQ. It will save the information sent to the
   microservice locally


   

Here are the basics of what we currently envision this microservice to do:

• JSON request "add"
• JSON request "search"
• JSON request "edit"
   - "add" option
   - "remove" option
• JSON request "delete"




How to set up the keyword manager microservice (Python for now, more will be included in the future!):

   1. install ZeroMQ to your system.
   2. install the microservice and run it.
      - it will run forever, once you are done using it, terminate the program
      - it will update to a new request once it is sent
   4. import ZeroMQ to the file that you wish to communicate with
      - import zmq
   6. set up the ZeroMQ context and socket:
      - context = zmq.Context()
      - socket = context.socket(zmq.REQ))
   7. set up the connection (right now the service runs locally, so "tcp://127.0.0.1:5555" will work)
      - don't worry, thats just localhost and the port 5555 is so it can communicate via your machine
   8. use one of the different requests below (if you're on python, they're plug and play)
   9. send the request over to the microservice
      - socket.send_json(request)
   10. set up a response:
      - response = socket.recv_json()
      - print(response)
   12. include socket.close() and context.term() after your print(response) in order to successfully end the connection
      



Basics of each function of the microservice:

• request = {
        "action": "add"
        "item_id": "your item's key"
        "keywords": "whatever","keywords"
  }

• request = {
        "action": "search"
        "keyword": "keyword"
  }

• request = {
        "action": "edit"
        "operation": "add_keyword" -or- "remove_keyword"
        "item_id": "item's key"
        "keywords": "keywords", "in", "question"
  }

• request = {
              "action": "delete"
              "item_id": "item's key"
  }



