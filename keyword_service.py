# This program now uses ZeroMQ to perform its communication with a main program.
# The main functions are as follows:
#       - receives the item and keyword associated with it in a request with JSON data.
#       - the microservice saves the received keyword and ticket to a .json file locally.
#       - when a user gives a search query (request) with a given keyword, the microservice
#         will return whatever items are associated with the keyword.

import zmq
import json
import os

# this is either the re-initialization of a previous keywords json file,
# or it will create an entirely new keywords json file if there is not one
if os.path.exists("keywords.json"):
    with open("keywords.json", "r") as file:
        keyword_storage = json.load(file)
else:
    keyword_storage = {}


# creates the socket and the environment for said socket
context  = zmq.Context()
socket   = context.socket(zmq.REP)


# this is the socket the microservice will receive connections with
socket.bind("tcp://127.0.0.1:5555")


# this is what allows the microservice to wait for incoming requests,
# when it receives JSON data, it will print Received and send a success
# back
while True:
    request = socket.recv_json()
    print("Received: ", request)

    action = request.get("action")


    #
    # ADD SECTION
    #

    # this is the check for the add feature, as well as a brief error
    # handling method using .get() to verify whether the keyword request
    # actually exists. If the item_id or keyword does not exist,
    # it returns None.
    if action == "add":
            item_id  = request.get("item_id")
            keywords = request.get("keywords")

            # piggybacking off the prior error handling, if either the
            # item_id or the keywords fields are empty, it will display
            # this
            if item_id is None:
                socket.send_json({
                    "success": False, "error": "Missing Entry: item_id"
                })
                continue

            # check for an invalid data type for item_id
            if not isinstance(item_id, str):
                socket.send_json({
                    "success": False, "error": "Invalid Type: item_id must be a string"
                })
                continue

            # checks if item_id is blank
            if len(item_id) == 0:
                socket.send_json({
                    "success": False, "error": "Invalid Input: item_id cannot be empty"
                })
                continue

            if keywords is None:
                socket.send_json({
                    "success": False, "error": "Missing Entry: keywords"
                })
                continue

            # in the case of just a single keyword
            if isinstance(keywords, str):
                keywords = [keywords]

            # singular data-type check
            if not isinstance(keywords,list):
                socket.send_json({
                    "success": False, "error": "Invalid Type: keywords must be string or list"
                })
                continue

            # checks if the keywords section is empty
            if len(keywords) == 0:
                socket.send_json({
                    "success": False, "error": "Invalid Input: keywords cannot be empty"
                })
                continue

            # checks if any of the keywords in a list are the correct data type
            invalid_type_keyword = False
            for keyword in keywords:
                if not isinstance(keyword, str):
                    invalid_type_keyword = True
                    break

            # if there is a non-string in the list, an error will be thrown
            if invalid_type_keyword is True:
                socket.send_json({
                    "success": False, "error": "Invalid Type: keywords must be a string"
                })
                continue

            if item_id in keyword_storage:
                socket.send_json({
                    "success": False, "error": "Invalid Entry: Item already exists!"
                })
                continue

            # the action that actually adds the keyword to the dictionary
            keyword_storage[item_id] = keywords

            # creates the .json file to which it will write all the items from the
            # keyword_storage dictionary as JSON data
            with open("keywords.json", "w") as file:
                json.dump(keyword_storage, file, indent=4)
            socket.send_json({
                "success": True, "Confirmed": " Your Ticket has been submitted!"
            })


    #
    # SEARCH SECTION
    #

    #this is the check for the search feature
    elif action == "search":

        # this initializes an empty list to store matched keywords
        matches = []
        searched_keyword = request.get("keyword")

        # Same as in the add section, when the keyword
        # request is none, it will display this
        if searched_keyword is None:
            socket.send_json({
                "success": False, "error": "Keyword Field Empty"
            })
            continue

        # data-type check
        if not isinstance(searched_keyword, str):
            socket.send_json({
                "success": False, "error": "Invalid Type: Search keyword must be a string!"
            })
            continue

        if len(searched_keyword) == 0:
            socket.send_json({
                "success": False, "error": "Search keyword cannot be empty!"
            })
            continue

        # simple loop to search through the dictionary in the microservice
        for item_id, keywords in keyword_storage.items():
            if searched_keyword in keywords:
                # saves the keywords in the empty matches[] list
                matches.append(item_id)

        # when the microservice is done searching, it will return the matches
        socket.send_json({
            "success": True, "item_ids": matches
        })


    #
    # EDIT SECTION
    #

    # check for the edit section
    elif action == "edit":
        operation = request.get("operation")
        item_id = request.get("item_id")
        keywords = request.get("keywords")

        # these are the same error checks as in the add section, with the
        # addition of operation
        if operation is None:
            socket.send_json({
                "success": False, "error": "Missing Entry: operation"
            })
            continue
        if item_id is None:
            socket.send_json({
                "success": False, "error": "Missing Entry: item_id"
            })
            continue

        # check for an invalid data type for item_id
        if not isinstance(item_id, str):
            socket.send_json({
                "success": False, "error": "Invalid Type: item_id must be a string"
            })
            continue

        # checks if item_id is blank
        if len(item_id) == 0:
            socket.send_json({
                "success": False, "error": "Invalid Input: item_id cannot be empty"
            })
            continue

        if keywords is None:
            socket.send_json({
                "success": False, "error": "Missing Entry: keywords"
            })
            continue

        # checks for the item in the dictionary
        if item_id not in keyword_storage:
            socket.send_json({
                "success": False, "error": "Item Does Not Exist"
            })
            continue

        # in the case of just a single keyword
        if isinstance(keywords, str):
            keywords = [keywords]

        # data-type check
        if not isinstance(keywords, list):
            socket.send_json({
                "success": False, "error": "Invalid Type: Keywords must be string or list"
            })
            continue

        # checks if any of the keywords in a list are the correct data type
        invalid_type_keyword = False
        for keyword in keywords:
            if not isinstance(keyword, str):
                invalid_type_keyword = True
                break

        if invalid_type_keyword is True:
            socket.send_json({
                "success": False, "error": "Invalid Type: Keywords must be a string"
            })
            continue


        #
        # ADD_KEYWORD SECTION
        #

        # adds the specified keyword to the existing item in the .json file
        if operation == "add_keyword":

            # empty list check
            if len(keywords) == 0:
                socket.send_json({
                    "success": False, "error": "keywords cannot be empty!"
                })
                continue

            # error handling in case the specified keyword already exists with
            # that item, if it doesn't, it appends it to the item
            for keyword in keywords:
                if keyword in keyword_storage[item_id]:
                    continue
                else:
                    keyword_storage[item_id].append(keyword)

            with open("keywords.json", "w") as file:
                json.dump(keyword_storage, file, indent=4)
            socket.send_json({
                "success": True, "Confirmed": "Your keyword has been added to the ticket!"
            })


        #
        # REMOVE_KEYWORD SECTION
        #

        # removes the specified keyword(s) to from existing item in the .json file
        elif operation == "remove_keyword":
            # empty list check
            if len(keywords) == 0:
                socket.send_json({
                    "success": False, "error": "keywords cannot be empty!"
                })
                continue

            # keyword removal
            for keyword in keywords:
                if keyword in keyword_storage[item_id]:
                    keyword_storage[item_id].remove(keyword)

            with open("keywords.json", "w") as file:
                json.dump(keyword_storage, file, indent=4)
            socket.send_json({
                "success": True, "Confirmed": "The keyword has been removed from the ticket!"
            })

        # if the operation tag does not include add or remove, an error is thrown
        else:
            socket.send_json({
                "success": False, "error": "Invalid Input: Expected 'add_keyword' or 'remove_keyword'"
            })
            continue


    #
    # DELETE SECTION
    #

    # checks for delete request
    elif action == "delete":
        item_id = request.get("item_id")

        # the same error handling as prior sections
        if item_id is None:
            socket.send_json({
                "success": False, "error": "Missing Entry: item_id"
            })
            continue

        # check for an invalid data type for item_id
        if not isinstance(item_id, str):
            socket.send_json({
                "success": False, "error": "Invalid Type: item_id must be a string"
            })
            continue

        # checks if item_id is blank
        if len(item_id) == 0:
            socket.send_json({
                "success": False, "error": "Invalid Input: item_id cannot be empty"
            })
            continue

        if item_id not in keyword_storage:
            socket.send_json({
                "success": False, "error": "Item Does Not Exist"
            })
            continue

        # deletes the item from the dictionary and updates the json file
        del keyword_storage[item_id]
        with open("keywords.json", "w") as file:
            json.dump(keyword_storage, file, indent=4)
        socket.send_json({
            "success": True, "Confirmed": " Your Ticket has been deleted!"
        })


    # if the request includes actions not present in the microservice, this
    # displays
    else:
        socket.send_json({
            "success": False, "error": "Invalid Action: Expected 'add', 'search', 'edit', or 'delete'"
        })









