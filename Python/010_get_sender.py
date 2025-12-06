#!/usr/bin/env python3
import requests
import json # This library helps print the response nicely

# The test URL that will echo our request
target_url = "https://httpbin.org/get"

# The data we want to send as GET parameters, defined as a dictionary
payload = {
    "item": "python script",
    "version": "1.0",
    "author": "inugasuki44"
}

print(f"--- Sending GET request to {target_url} ---")

try:
    # Send the GET request, passing our dictionary to the 'params' argument
    response = requests.get(target_url, params=payload)
    # This will raise an error if the request was unsuccessful (e.g., 404, 500)
    response.raise_for_status()

    # Print the full URL that was actually constructed and sent
    print(f"\nConstructed URL: {response.url}\n")

    # The server responds with JSON data. We parse it and print it neatly.
    print("--- Server Response ---")
    # response.json() converts the JSON response into a Python dictionary
    # json.dumps() formats the dictionary for easy reading
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")