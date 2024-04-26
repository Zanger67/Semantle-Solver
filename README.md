> This is a still in-progress project

# Semantle Solver

[Semantle.com](https://semantle.com/) is a word game inspired by Woordle based around guessing the day's term bsaed off of it's meaning and word association rather than spelling and letters. Users are given a "score" of how close their guesses are based on a cosine similarity calculation, and are given infinite guesses (meaning games can go upwards of hundreds of guesses depending on the word).

This program will proceed to query the server for the word vector files and calculate the same values that the website gives players, and use them to guess the word by checking internet queries to draw connections.





## Notes
Since Semantle's website doesn't attempt to prevent the word from being known if you check inspect element, this program will run off of the assumption of ignorance. That is, it will make use of the day's word when necessary for pinging the server but pretend as if it doesn't know the word as it does its own calculations and guesses.