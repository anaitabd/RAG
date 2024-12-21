import pymongo
import requests
import time

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://abdallahnaitabdallah:gKMhysrtTi8Wr0GZ@rag.irwur.mongodb.net/?retryWrites=true&w=majority&appName=RAG")
db = client.sample_mflix
collection = db.movies

# Hugging Face API details
hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

# Generate embeddings with retry mechanism
def generate_embedding(text: str, retries: int = 5, delay: int = 5) -> list[float]:
    for attempt in range(retries):
        response = requests.post(
            embedding_url,
            headers={"Authorization": f"Bearer {hf_token}"},
            json={"inputs": text}
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:  # Model loading
            estimated_time = response.json().get("estimated_time", delay)
            print(f"Model loading, retrying in {estimated_time} seconds...")
            time.sleep(estimated_time)
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            break
    return []  # Return empty list if retries exhausted

# Process documents and update embeddings
def update_embeddings():
    for doc in collection.find({'plot': {"$exists": True}}, {"_id": 1, "plot": 1}):
        try:
            embedding = generate_embedding(doc['plot'])
            if embedding:  # Only update if embedding was successfully generated
                doc['plot_embedding_hf'] = embedding
                collection.replace_one({'_id': doc['_id']}, doc)
                print(f"Updated embedding for document ID: {doc['_id']}")
            else:
                print(f"Failed to generate embedding for document ID: {doc['_id']}")
        except Exception as e:
            print(f"Error processing document ID: {doc['_id']}, Error: {e}")


if __name__ == "__main__":
    query = "imaginary characters from outer space at war"

    results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector": generate_embedding(query),
        "path": "plot_embedding_hf",
        "numCandidates": 100,
        "limit": 4,
        "index": "PlotSemanticSearch",
        }}
    ])

    for document in results:
        print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')