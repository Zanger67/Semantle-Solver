


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




- since the URL to retrieve the vector file is based off of the target SECRET word, we must query it at least one initially to get the secret word and just not use it...









# Sections of website code:

```js
// line 224) in function guessRow(similarity, oldGuess, percentile, guessNumber, guess, player, isLocal = true) {

    let guessType = percentile === 1000 ? 'word-found' : 'word-cold';
    guessType = percentile < 1000 ? 'word-close' : guessType;
    guessType = percentile < 500 ? 'word-fire' : guessType;
    guessType = percentile < 250 ? 'word-glass' : guessType;
    guessType = percentile < 1 && similarity >= 20 ? 'word-glass' : guessType;
    guessType = percentile < 1 && similarity < 20 ? 'word-cold' : guessType;
```


```js
// line 1009 --> updateGuesses() --> calls guessRow and holds percentiles
for (let entry of guesses) {
    let [similarity, oldGuess, percentile, guessNumber, player, localGuess] = entry;
    if (oldGuess === latestGuess) {
        inner += guessRow(similarity, oldGuess, percentile, guessNumber, latestGuess, player, localGuess);
    }
}
```


```js
// line 669 --> doGuess function
const guessData = await getModel(guess);
if (!guessData) {
    $('#error').textContent = `I don't know the word ${guess}.`;
    return false;
}


// line 474 async function --> getModel --> calling the website we noted
async function getModel(word) {
    if (cache.hasOwnProperty(word)) {
        return cache[word];
    }
    const url = "/model2/" + secret + "/" + word.replace(/\ /gi, "_");
    const response = await fetch(baseUrl + url);
    try {
        const result = await response.json();
        if (result) {
            cache[guess] = result;
        }
        return result;
    } catch (e) {
        return null;
    }
}
/* 
 * CONST URL --> retrieves the url where the first is the target value itself
 * value 2 is the guess
 * Thus the output json file is a file that is catered specifically remotely for this case
 */

// specifically found in this line:
    const url = "/model2/" + secret + "/" + word.replace(/\ /gi, "_");

```




Similarity output is the cosine similarity of the actual value vector and the guess
> *note that we also take the percentile value or 0 --> top 1000 values?*

```js
// Line 672 ish

        let percentile = guessData.percentile || 0;

        const guessVec = guessData.vec;

        let similarity = getCosSim(guessVec, secretVec) * 100.0;
        if (!guessed.has(guess)) {
            if (!gameOver) {
                guessCount += 1;
            }
            guessed.add(guess);

            const newEntry = [similarity, guess, percentile, guessCount,...
```
This means we need to store the actual value to calculate the similarity scores :l






```js
//line 43 gets secret word
function getSecretWord(day) {
    let pn = getWordIndex(getPuzzleNumber(day));
    return secretWords[pn];
}


// selects word line 83
let ptoday = queryPuzzleDay ? Number(queryPuzzleDay) + initialDay : (puzzleDay ? Number(puzzleDay) : today);
```