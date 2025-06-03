from sentence_transformers import SentenceTransformer
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import numpy as np
from tqdm import tqdm

# Loading the entire dataset
df = pd.read_csv("source/LinkedIn_posts.csv")
print(f"Loaded {len(df)} records")

# Loading BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connecting to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Creating a collection (need to know the dimension of vectors)
# Create an example embedding to find out the dimension
sample_embedding = model.encode(["Sample text"])
vector_size = sample_embedding.shape[1]

# Creating collection
client.recreate_collection(
    collection_name="linkedin-posts",
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
)

BATCH_SIZE = 100

# Processing data in batches
for batch_start in tqdm(range(0, len(df), BATCH_SIZE)):
    # Determining the end of the current batch
    batch_end = min(batch_start + BATCH_SIZE, len(df))

    # выделение chasti dataframe
    batch_df = df.iloc[batch_start:batch_end]

    # Creating embeddings for the current batch
    batch_texts = batch_df["post_text"].tolist()
    batch_embeddings = model.encode(batch_texts, show_progress_bar=False)

    # Preparing points for loading
    points = [
        PointStruct(
            id=batch_start + i,  # Global ID for the entire dataset
            vector=batch_embeddings[i],
            payload={"text": batch_texts[i], "date": batch_df["date_posted"].iloc[i]}
        )
        for i in range(len(batch_texts))
    ]

    # Loading batch into collection
    client.upsert(collection_name="linkedin-posts", points=points)

    print(f"Loaded batch {batch_start // BATCH_SIZE + 1}: records {batch_start}-{batch_end - 1}")

print("Loading completed!")