from sentence_transformers import SentenceTransformer
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
import numpy as np
from tqdm import tqdm

# Загрузка всего датасета
df = pd.read_csv("source/LinkedIn_posts.csv")
print(f"Загружено {len(df)} записей")

# Загрузка модели BERT
model = SentenceTransformer("all-MiniLM-L6-v2")

# Подключение к Qdrant
client = QdrantClient(host="localhost", port=6333)

# Создание коллекции (требуется знать размерность векторов)
# Создадим пример эмбеддинга чтобы узнать размерность
sample_embedding = model.encode(["Sample text"])
vector_size = sample_embedding.shape[1]

# Создание коллекции
client.recreate_collection(
    collection_name="linkedin-posts",
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
)

# Определение размера батча
BATCH_SIZE = 100

# Обработка данных по батчам
for batch_start in tqdm(range(0, len(df), BATCH_SIZE)):
    # Определение конца текущего батча
    batch_end = min(batch_start + BATCH_SIZE, len(df))

    # Выделение части датафрейма
    batch_df = df.iloc[batch_start:batch_end]

    # Создание эмбеддингов для текущего батча
    batch_texts = batch_df["post_text"].tolist()
    batch_embeddings = model.encode(batch_texts, show_progress_bar=False)

    # Подготовка точек для загрузки
    points = [
        PointStruct(
            id=batch_start + i,  # Глобальный ID для всего датасета
            vector=batch_embeddings[i],
            payload={"text": batch_texts[i], "date": batch_df["date_posted"].iloc[i]}
        )
        for i in range(len(batch_texts))
    ]

    # Загрузка батча в коллекцию
    client.upsert(collection_name="linkedin-posts", points=points)

    print(f"Загружен батч {batch_start // BATCH_SIZE + 1}: записи {batch_start}-{batch_end - 1}")

print("Загрузка завершена!")