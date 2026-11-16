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

How to set up the keyword manager microservice:

   1. 



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



