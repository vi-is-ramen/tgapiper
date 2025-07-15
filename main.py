from scrap import scrap
from gen import gen
import os
import json


if __name__ == "__main__":
    print("Checking directories...")
    if not os.path.exists("tg"):
        os.makedirs("tg/types")
        os.makedirs("tg/methods")
    
    if not os.path.exists("tg/types"):
        os.makedirs("tg/types")
    
    if not os.path.exists("tg/methods"):
        os.makedirs("tg/methods")
    
    print("Cleaning up...")

    for filename in os.listdir("tg/types"):
        if filename.endswith(".py"):
            os.remove(f"tg/types/{filename}")
            
    for filename in os.listdir("tg/methods"):
        if filename.endswith(".py"):
            os.remove(f"tg/methods/{filename}")
    
    if os.path.exists("api.min.json"):
        os.remove("api.min.json")

    print("Scrapping...")
    scrap()
    with open("api.min.json", "r") as f:
        api_version = json.load(f)["version"]
    print(f"Telegram Bot API version: {api_version}")
    print("Generating...")
    gen()
    print("Creating statistics...")
    ntypes = 0
    nmethods = 0
    for filename in os.listdir("tg/types"):
        if filename.endswith(".py"):
            ntypes += 1
            
    for filename in os.listdir("tg/methods"):
        if filename.endswith(".py"):
            nmethods += 1

    print(f"Generated {ntypes-1} types and {nmethods-1} methods")

    print("Testing...")

    import test

    print("Done")
