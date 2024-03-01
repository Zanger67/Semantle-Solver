


Link to main website: [https://semantle.com/](https://semantle.com/)

Semantle pings for an input by sending: https://semantle.com/model2/bread/INSERT_WORD
Uses a keepalive HTTP connection

```url
https://semantle.com/model2/bread/INSERT_WORD
```

Response is a **JSON file**
- idk what the "bread" part is about

- JSON reply is in the form of...

```json
{"vec":[0.0, 0.0, 0.0, ..., 0.0]}
```
300 values ranging from -1.0 to +1.0
indices [0, 299]



Plans:
- use python:
```python
import requests
x = requests.get('insert url here')
```

see if this works with pandas --> if the request will output a json that i can assign to a variable

note:
```powershell
pip install requests
```

- Have a set of default random values or just get python to pull the most common words according to Google
    - pbly best to just have a starter set
- after that point, scrape familiar values off the internet by submitting google queries?
- maybe wikipedia would be better
- also possible to use gpt instead but that would cost money :l
- also could use google scholar and scrape articles


IMPORTANT
- Semantle uses `Word2vec` --> see if this applies to the 300 value vector taken
    - `Word2vec` is an NLP technique 
- account heavily if we find a "ranked" term

- *Dataset used: `GoogleNews-vectors-negative300.bin from late 2021`*


- have a set of "banned words" such as and, or, but, etc.

- create a file that just holds the url in case things change
- maybe something that tracks trends in answering? (like, oh past 5 guesses have each gone down in score so let's change directions)

- could also add a thing to find all 1000 top words if bored
- also could try to do this with other languages since they have the game in other languages



[Note](https://www.w3schools.com/python/module_requests.asp)

Method                          | Description
| :---------------------------- | :---- |
`delete(url, args)`             | Sends a DELETE request to the specified url
`get(url, params, args)`        | Sends a GET request to the specified url
`head(url, args)`               | Sends a HEAD request to the specified url
`patch(url, data, args)`        | Sends a PATCH request to the specified url
`post(url, data, json, args)`   | Sends a POST request to the specified url
`put(url, data, args)`          | Sends a PUT request to the specified url
`request(method, url, args)`    | Sends a request of the specified method to the specified url