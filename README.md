# Debugging Search Relevance

- A service that pictures how search engine "works" (with many simplifications obviously)
- You can think of this repo as a "mini" `ElasticSearch` (match & rank on inverted index)

# Requirements

- `Python 3.6` or above
- Install required libraries: `pip install -r requirements.txt`

# How to Run

- Start the engine: `cd` into the root directory and run `python3 app.py`
- The engine is wrapped using `flask` so you can access it using `POST` request (e.g. using `POSTMAN`)

- Example `/analyze` request:
```
curl --location --request POST 'http://localhost:8080/analyze' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "keywords": "beli hape asus"
}'
```
- Example `/analyze` result:
Note that the token `beli` is dropped and the token `hape` is normalized to `hp`
See `data/preprocessing/stopwords.txt` and `data/preprocessing/word_map.txt`
```
{
  "data": {
      "tokens": [
          "hp",
          "asus"
      ]
  }
}
```

- Example `/match` request:
```
curl --location --request POST 'http://localhost:8080/match' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "keywords": "asus"
  }'
```
- Example `/match` result:
Note that the token `beli` is dropped and the token `hape` is normalized to `hp`
See `data/preprocessing/stopwords.txt` and `data/preprocessing/word_map.txt`
```
{
    "data": {
        "products": [
            {
                "desc": "cocok untuk gaming: DotA, CSGO, dkk",
                "match": {
                    "asus": {
                        "desc": [
                            "10"
                        ],
                        "title": [
                            "10",
                            "11"
                        ]
                    }
                },
                "title": "Laptop ASUS VivoBook 15"
            },
            {
                "desc": "hp asus murah banget dah asli murah, asus is the best, beli asus !",
                "match": {
                    "asus": {
                        "desc": [
                            "10"
                        ],
                        "title": [
                            "10",
                            "11"
                        ]
                    }
                },
                "title": "ASUS ROG Phone 5"
            }
        ]
    }
}
```

- Example `/rank` request:
```
curl --location --request POST 'http://localhost:8080/rank' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "keywords": "asus"
}'
```
- Example `/rank` result:
Note that the token `beli` is dropped and the token `hape` is normalized to `hp`
See `data/preprocessing/stopwords.txt` and `data/preprocessing/word_map.txt`
```
{
    "data": {
        "products": [
            {
                "ID": "11",
                "desc": "cocok untuk gaming: DotA, CSGO, dkk",
                "scores": {
                    "final_score": 0.1013662770270411,
                    "idf": {
                        "desc": {
                            "asus": 1.0986122886681098
                        },
                        "title": {
                            "asus": 0.4054651081081644
                        }
                    },
                    "tf": {
                        "desc": {},
                        "title": {
                            "asus": 0.25
                        }
                    }
                },
                "title": "Laptop ASUS VivoBook 15"
            },
            {
                "ID": "10",
                "desc": "hp asus murah banget dah asli murah, asus is the best, beli asus !",
                "scores": {
                    "final_score": 0.030371519345029976,
                    "idf": {
                        "desc": {
                            "asus": 1.0986122886681098
                        },
                        "title": {
                            "asus": 0.4054651081081644
                        }
                    },
                    "tf": {
                        "desc": {
                            "asus": 0.2727272727272727
                        },
                        "title": {
                            "asus": 0.25
                        }
                    }
                },
                "title": "ASUS ROG Phone 5"
            }
        ]
    }
}
```
