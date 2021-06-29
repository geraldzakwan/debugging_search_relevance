# Debugging Search Relevance

- A service that pictures how search engine "works" (with many simplifications obviously)
- You can think of this repo as a "mini" `ElasticSearch` (match & rank on inverted index)

# Requirements

- `Python 3.6` or above
- Install required libraries: `pip install -r requirements.txt`

# How to Run

- Start the engine: `cd` into the root directory and run `python3 app.py`
- The engine is wrapped using `flask` so you can access it using `POST` request
- Example request:
```
  curl --location --request POST 'http://localhost:8080/query' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "keywords": "hp asus"
  }'
```
- Example result:
```
  {
      "data": {
          "products": [
              {
                  "desc": "hp asus murah banget dah asli murah",
                  "title": "hp asus murah banget dah asli murah"
              }
          ]
      }
  }
```
