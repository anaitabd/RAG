# Movie Recommendation System

This project demonstrates a movie recommendation system using MongoDB and Hugging Face for semantic search. It generates embeddings for movie plots and allows querying the database to find movies with similar plot descriptions.

## Features
- Connects to a MongoDB database to store and retrieve movie data.
- Uses Hugging Face API to generate embeddings for movie plots.
- Implements semantic search using MongoDB's vector search capabilities.

## Prerequisites

- Python 3.8 or higher
- MongoDB with vector search enabled
- Hugging Face account for API access

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/anaitabd/RAG.git
    cd RAG
    ```

2. Create a `.env` file to store environment variables:
    ```env
    MONGODB_USER=your_mongodb_username
    MONGODB_PASSWORD=your_mongodb_password
    HF_TOKEN=your_hugging_face_api_token
    ```

3. Install dependencies:
    ```bash
    pip install pymongo requests python-dotenv
    ```

## Usage

### 1. Generating Plot Embeddings
The script retrieves movie plots from the MongoDB collection and generates embeddings using the Hugging Face API. These embeddings are then stored in the database.

Run the script to generate embeddings:
```bash
python script_name.py
```

### 2. Querying the Database
The script allows querying the database with a description, e.g., "imaginary characters from outer space at war". The vector search feature in MongoDB retrieves movies with similar plots.

Example:
```python
query = "imaginary characters from outer space at war"
```

### 3. Example Output
The system will return a list of matching movies, displaying the title and plot for each.

```plaintext
Movie Name: Star Wars,
Movie Plot: A long time ago in a galaxy far, far away...

Movie Name: Guardians of the Galaxy,
Movie Plot: A group of intergalactic criminals must pull together...
```

## Key Components

### MongoDB Connection
- Connects to a MongoDB cluster using credentials stored in the `.env` file.
- Requires a MongoDB database with a collection named `movies`.

### Hugging Face Integration
- Generates embeddings for movie plots using the Hugging Face API.
- API URL: `https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2`

### Semantic Search
- Performs vector-based semantic search on the `plot_embedding_hf` field in the MongoDB collection.

## Troubleshooting

### Common Errors
1. **503 Model Loading Error**:
   - The Hugging Face model may take time to load. The script retries embedding generation if the model is unavailable.

2. **Connection Error**:
   - Ensure MongoDB credentials in the `.env` file are correct.
   - Check network connectivity and ensure MongoDB is accessible.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

