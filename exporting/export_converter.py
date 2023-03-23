import os
import json
import datetime
from datetime import datetime as dt

defined_users = {
    
    # id: {
        # name: int
        # aliases: []
    # }
    
    312119266956804100: {
        "name": "isaac",
        "aliases": ["iski", "isis", "zacin", "zacin8or"]
    },
    
    320215256355831830: {
        "name": "chris",
        "aliases": ["chrizzo"]
    },
    
    415391440001040384: {
        "name": "alessia",
        "aliases": ["deku meister", "deku", "alessio", "alessi"]
    },
    
    415391440001040384: {
        "name": "matthew",
        "aliases": ["matt", "cattmatt", "natt", "mart"]
    },
    
    520069172974190602: {
        "name": "kris",
        "aliases": ["it's not a phase"]
    },
    
    857123038414504006: {
        "name": "kaitlin",
        "aliases": ["soymilk"]
    },

    337099649884356628: {
        "name": "aiden",
        "aliases": ["hi i'm aiden", "hi im aiden"]
    }
}



coversations_folder = r"exporting/conversations/"
chat_history_file = r"exporting/general1.json"

with open(chat_history_file, "r", encoding="utf8") as chat_history:
    
    chat_history = json.load(chat_history)
    messages = chat_history["messages"]
    pass

conversations_files = []

current_conversation = [
    # {
        # id = 0000
        # content = ""
        # author = 0000
        # trigger_replies = []   
    # }
]
prev_time = dt.strptime(messages[0]["timestamp"].split(".")[0].split("+")[0], "%Y-%m-%dT%H:%M:%S") - datetime.timedelta(seconds=5)
num_conversations_base = 0
num_conversations = 0


for message in messages:
    
    curr_time = dt.strptime(message["timestamp"].split(".")[0].split("+")[0], "%Y-%m-%dT%H:%M:%S")
    author_id = int(message["author"]["id"])
    
    if message["type"] == "Reply":
        
        #print("Replied!")
        
        reply_id = int(message["reference"]["messageId"])
        
        for i in current_conversation:
            
            
            if i["id"] == reply_id:
                
                i["trigger_replies"].append(author_id)
                break
                
        else:
            
            
            
            for filename in conversations_files.copy():
                
                start_id, end_id = filename.split(" ")[1].split("~")
                
                start_id = int(start_id)
                end_id = int(end_id)
                
                if reply_id >= start_id and reply_id <= end_id:
                    
                    print("Uh oh")
                    
                    with open(coversations_folder + filename + ".json", "r", encoding="utf8") as chat_history:
    
                        chat_history = json.load(chat_history)

                    found = False
                    for i in chat_history:
            
                        if i["id"] == reply_id:
                            
                            i["trigger_replies"].append(author_id)
                            found = True
                            break
                        
                    if found == True:
                        
                        temp_filename = "0" * (6 - len(str(num_conversations))) + str(num_conversations) + " " + str(current_conversation[0]["id"]) + "~" + str(current_conversation[-1]["id"])
        
                        conversations_files.append(temp_filename)
                        
                        with open(coversations_folder + temp_filename + ".json", "w", encoding="utf8") as write_file:
                            
                            json.dump(current_conversation, write_file, indent=4)
                        
                        num_conversations_base += 1
                        num_conversations = int(filename.split(" ")[0])
                        current_conversation = chat_history
                        
                        os.remove(coversations_folder + filename + ".json")
                        conversations_files.remove(filename)
                        
                        break
                        
    
    if (curr_time - prev_time) > datetime.timedelta(minutes=45) :
        
        filename = "0" * (6 - len(str(num_conversations))) + str(num_conversations) + " " + str(current_conversation[0]["id"]) + "~" + str(current_conversation[-1]["id"])
        
        conversations_files.append(filename)
        
        with open(coversations_folder + filename + ".json", "w", encoding="utf8") as write_file:
            
            json.dump(current_conversation, write_file, indent=4)
        
        current_conversation = []
        num_conversations_base += 1
        num_conversations = num_conversations_base
    
    if (curr_time - prev_time) < datetime.timedelta(seconds=1):
        if len(current_conversation) > 1:
            current_conversation[-2]["trigger_replies"].append(author_id)
    else:
        if len(current_conversation) > 0:
            current_conversation[-1]["trigger_replies"].append(author_id)
    
    
    current_conversation.append(
        {
            "id": int(message["id"]),
            "content": message["content"],
            "author": author_id,
            "time": curr_time.strftime("%Y-%m-%dT%H-%M-%S"),
            "trigger_replies": []
        }
    )
        
    prev_time = curr_time
            
        
prev_conversation = ""
prev_end_id = 0

print("-END-")

for i in conversations_files:
    
    start_id, end_id = i.split(" ")[1].split("~")
    
    start_id = int(start_id)
    end_id = int(end_id)
    
    if start_id <= prev_end_id:
        
        print("1. " + prev_conversation + "\n2. " + i + "\n")
    
    prev_conversation = i
    prev_end_id = end_id
    
