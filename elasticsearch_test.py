from elasticsearch import Elasticsearch

# Elasticsearch connection
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Function to search Elasticsearch
def search_es(query):
    """Search Elasticsearch for relevant documents."""
    body = {
        "query": {
            "match_phrase": {
                "text": {
                    "query": query,
                }
            }
        }
    }
    
    # Replace 'your_index_name' with the actual index name you're using
    index_name = "my_index"  # Modify this with the correct index name
    response = es.search(index=index_name, body=body)
    
    # Extract the hits from the Elasticsearch response
    hits = response['hits']['hits']
    
    return [(hit['_source']['text'], hit['_score']) for hit in hits]

# Test Elasticsearch query
query = "What is the future of India?"
es_results = search_es(query)

# Display Elasticsearch results
for idx, (text, score) in enumerate(es_results, 1):
    print(f"Result {idx}: {text} (Score: {score})")
