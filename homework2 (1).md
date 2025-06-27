
# Homework: Vector Search

In this homework, we will learn more about vector search and embedding. Like in the module, we will use Qdrant and fastembed.

It's possible that your answers won't match exactly. If it's the case, select the closest one.

**Note:** if you want to learn how vector search works under the hood, check homework 3 from the 2024 cohort (questions 1-4)

---

## Embeddings

Qdrant uses `fastembed` under the hood to turn text into vectors.

We will now explore this library.

Make sure it's installed:

```bash
pip install fastembed
```

Import it:

```python
from fastembed import TextEmbedding
```

---

### Q1. Embedding the query

Embed the query: `'I just discovered the course. Can I join now?'` using the `jinaai/jina-embeddings-v2-small-en` model.

You should get a numpy array of size 512.

**What's the minimal value in this array?**

- -0.51  
- ✅ -0.11  
- 0  
- 0.51  

---

## Cosine similarity

The vectors that our embedding model returns are already normalized: their length is 1.0.

You can check that by using the norm function:

```python
import numpy as np
np.linalg.norm(q)
```

Which means that we can simply compute the dot product between two vectors to learn the cosine similarity between them.

For example, if you compute the cosine of the query vector with itself, the result will be 1.0:

```python
q.dot(q)
```

---

### Q2. Cosine similarity with another vector

Now let's embed this document:  
`doc = 'Can I still join the course after the start date?'`

**What's the cosine similarity between the vector for the query and the vector for the document?**

- 0.3  
- 0.5  
- ✅ 0.7  
- 0.9  

---

### Q3. Ranking by cosine

Compute the embeddings for the `text` field, and compute the cosine between the query vector and all the documents.

**What's the document index with the highest similarity? (Indexing starts from 0):**

- ✅ 0  
- 1  
- 2  
- 3  
- 4  

---

### Q4. Ranking by cosine, version two

Now let's calculate a new field:

```python
full_text = doc['question'] + ' ' + doc['text']
```

Embed this field and compute the cosine between it and the query vector.

**What's the highest scoring document?**

- ✅ 0  
- 1  
- 2  
- 3  
- 4  

**Is it different from Q3? If yes, why?**

✅ The winning document is the same (index 0), but the similarity score is higher because combining the question and answer gives a fuller context for the embedding model to interpret.

---

### Q5. Selecting the embedding model

**What's the smallest dimensionality for models in fastembed?**

- 128  
- 256  
- ✅ 384  
- 512  

Model used: `BAAI/bge-small-en`

---

### Q6. Indexing with Qdrant (2 points)

We will now use more documents:

```python
import requests 

docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']
    if course_name != 'machine-learning-zoomcamp':
        continue

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)
```

Add them to Qdrant using the model from Q5.

When adding the data, use both `question` and `text` fields:

```python
text = doc['question'] + ' ' + doc['text']
```

After inserting the data, query the collection using the query from Q1.

**What's the highest score in the results?**

- 0.97  
- 0.87  
- 0.77  
- ✅ 0.67  
