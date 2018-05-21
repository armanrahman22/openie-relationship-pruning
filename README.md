# Open Information Extraction Relationship Pruning

## What's this?

This is a dockerized web service to help prune the spurious [Open Information Extraction (OpenIE)](https://en.wikipedia.org/wiki/Open_information_extraction) relations
often generated by ClauseIE, Stanford CoreNLP, etc. For a quick way to deploy a dockerized ClauseIE server check out this [repo](https://github.com/c-w/ClausIE-Server) by Clemens Wolff. 

These parsers overgenerate relationships so the end user has more control over choosing the ones they want. 
For example from the sentence: "Virginia Woolf pioneered the use of stream of consciousness" they may produce the following relationship tuples:
```txt
(Virginia Woolf, pioneered, the use), 
(Virginia Woolf, pioneered, the use of stream), 
(Virginia Woolf, pioneered, the use of stream of consciousness)
```

In this case we would likely only want the last of these relations. This project contains methods for pruning these relations
using the idea of [domination](https://en.wikipedia.org/wiki/Dominating_decision_rule) from [Decision Rule Theory](https://en.wikipedia.org/wiki/Decision_rule).
The general idea is, if choosing between realtionships, to choose the one that contains at least the same information as the others and is the longest.
In the example above this would be:
```txt
(Virginia Woolf, pioneered, the use of stream of consciousness)
```

In addition this project prunes relations that are circular (subject and object are the same), relations with entities that are too short (like "it"),
and relations that contain [stop words](https://en.wikipedia.org/wiki/Stop_words). The latter two filters are configurable.

## Usage

Run the relationship pruning server via docker:

```sh
docker run -d -p 8000:8000 arrahm/openie-relationship-pruning
```

The server takes as input a [jsonl](http://jsonlines.org/) file where each line in the file is a json string representing a relationship tuple. For example:

```jsonl
{"argument":"the use", "line":0, "subject":"Virginia Woolf", "relation":"pioneered"}
{"argument":"the use of stream", "line":0, "subject":"Virginia Woolf", "relation":"pioneered"}
{"argument":"the use of stream of consciousness","line":0,"subject":"Virginia Woolf","relation":"pioneered"}
```
Note that the input requires each json line to contain fields for "argument", "subject", and "relation".

In order to send the file to the server the jsonl file should be passed as `multipart/form-data` under the form key `upload`:

```sh
curl -F "upload=@relationships.jsonl" "http://localhost:8000/prune/form"
```

The server will return a list of filtered relations in jsonl format:

```jsonl
{"argument":"the use of stream of consciousness","line":0,"subject":"Virginia Woolf","relation":"pioneered"}
```

## License

* MIT License
