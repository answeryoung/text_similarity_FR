# **Text Similarity** *--Fetch Rewards Coding Exercise*

**Da Yang** - dayang.phd@gmail.com

## Objective

Given two texts, this app scores their similarity. The score is at least 0.00 and at most 1.00. If the score is less than 0.20, a list of common words shall be listed.

This exercise is solved using Python, Flask, and Docker.

## Approach

Extending from class `difflib.SequenceMatcher`, I define a method `score()` that returns a `score` for any given pair of sentences ( `List[str]` ).

To calculate the score, I first get the matching code using the method `get_opcodes()`, which belongs to the base class. Then I attempt to expand all contracted words to the full length, i.e., "We've been to the moon!" -> "We have been to the moon!".  Last, the score is calculated as the ratio between the number of matched words and the geometric mean of the numbers of words in the given sentences.

Moreover, the input texts are broken into a list of sentences, which are lists of words, i.e., `List[List[str]]`, such that methods in `SequenceMatcher` can do their work.

Furthermore, if the numbers of sentences are not the same or the similarity score is below 0.20, a list of common words is returned. No score will be given for the former case.

## Demo

https://youtu.be/v77pNlvfD3k

## Set-up and run

`Python3` and `Flask` are needed in order to use this repo.  
`python3 app.py` would spin up a server bound to `http://127.0.0.1:5000/`  

To assemble a Docker image use `build_image.sh`, then use `run_image.sh` to run.  
The name of the docker image is `text_similarity:latest`.
The docker server would be bound to `http://localhost:5000/`.  
Docker needs to be installed first.

## Repo Structure

```repo
├── README.md     
|
├── app.py                          defines the Flask app, also contains the 
|                                   driver code
|
├── sequence_referee.py             a class extended from extended from
|                                   the class difflib.SequenceMatcher
├── text_similarity_utils.py        methods spliting_text(), topic_matcher(),
|                                   and join_sentence() are defined here
├── _mappings.py                    contains data for interpreting the
|                                   English language
|
├── Dockerfile                      Use this file to assemble a Docker image
├── build_image.sh                  Builds a docker image, text_similarity:latest
├── run_image.sh                    Runs the docker image in detached mode
|
├── templates                       HTML templates for the flask app
|   └── input.html                  
|   └── result.html
```
