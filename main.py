import os
import requests
import json
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class TODOmo:
    name: str
    content: str
    tags: list[str]

# Load environment variables
load_dotenv()

def request(method, url, data=None, params=None):
    # Wrapper method for requests lib
    # Automatically add url, api version and authorization to request
    url = os.getenv("BASE_URL") + os.getenv("API_VERSION") + url
    headers = {
        "Authorization": f"Bearer {os.getenv('TOKEN')}"
    }
    if data is not None:
        data = json.dumps(data)
        headers["Content-Type"] = "application/json"
    return requests.request(method, url, data=data, headers=headers, params=params)

def get_todomos():
    # Get username and also just check the token works
    r = request("GET", "/auth/me")
    if r.status_code != 200:
        return list()
    username = r.json()["user"]["name"]

    # Get memos tagged with "todomos" and map to a simplified object
    r = request("GET", f"/memos", params={"filter": f"\"todomos\" in tags && creator == \"{username}\""})
    return map(
        lambda todomo: TODOmo(todomo["name"], todomo["content"], todomo["tags"]),
        r.json()["memos"]
    )

def create_todomo(content, tags):
    tags.insert(0, "todomos")
    content = " ".join(map(lambda s: "#" + s, tags)) + "\n" + content + "\n\n*Created by TODOmos.*"
    return TODOmo(
        None,
        content,
        tags
    )

def post_todomo(todomo):
    r = request("POST", "/memos", data={
        "content": todomo.content,
        "visibility": "PRIVATE",
        "state": "NORMAL"
    })
    print(r.status_code)

def main():
    t = create_todomo("This todomo is a test.", ["hello", "goodbye"])
    post_todomo(t)
#    for todomo in get_todomos():
#        print(todomo)

if __name__ == "__main__":
    main()
