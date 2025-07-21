# Homework: Search Evaluation

In this homework, we will evaluate the results of vector search.

It's possible that your answers won't match exactly. If it's the case, select the closest one.

Required libraries  
We will use minsearch and Qdrant. Make sure you have the most up-to-date versions:

```
pip install -U minsearch qdrant_client
```

minsearch should be at least 0.0.4.

Evaluation data  
For this homework, we will use the same dataset we generated in the videos.

Let's get them:

```python
import requests
import pandas as pd

url_prefix = 'https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/03-evaluation/'
docs_url = url_prefix + 'search_evaluation/documents-with-ids.json'
documents = requests.get(docs_url).json()

ground_truth_url = url_prefix + 'search_evaluation/ground-truth-data.csv'
df_ground_truth = pd.read_csv(ground_truth_url)
ground_truth = df_ground_truth.to_dict(orient='records')
```

Here, documents contains the documents from the FAQ database with unique IDs, and ground_truth contains generated question-answer pairs.

Also, we will need the code for evaluating retrieval:

```python
from tqdm.auto import tqdm

def hit_rate(relevance_total):
    cnt = 0
    for line in relevance_total:
        if True in line:
            cnt = cnt + 1
    return cnt / len(relevance_total)

def mrr(relevance_total):
    total_score = 0.0
    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == True:
                total_score = total_score + 1 / (rank + 1)
    return total_score / len(relevance_total)

def evaluate(ground_truth, search_function):
    relevance_total = []
    for q in tqdm(ground_truth):
        doc_id = q['document']
        results = search_function(q)
        relevance = [d['id'] == doc_id for d in results]
        relevance_total.append(relevance)
    return {
        'hit_rate': hit_rate(relevance_total),
        'mrr': mrr(relevance_total),
    }
```

---

## Q1. Minsearch text  
Now let's evaluate our usual minsearch approach, but tweak the parameters. Let's use the following boosting params:

```python
boost = {'question': 1.5, 'section': 0.1}
```

What's the hitrate for this approach?

- 0.64  
- 0.74  
- 0.84  
- 0.94  

**Answer: 0.84**

---

## Q2. Vector search for question  
Now let's index these embeddings with minsearch:

```python
vindex = VectorSearch(keyword_fields={'course'})
vindex.fit(X, documents)
```

Evaluate this search method. What's MRR for it?

- 0.25  
- 0.35  
- 0.45  
- 0.55  

**Answer: 0.35**

---

## Q3. Vector search for question and answer  
We only used question in Q2. We can use both question and answer:

Evaluate the performance. What's the hitrate?

- 0.62  
- 0.72  
- 0.82  
- 0.92  

**Answer: 0.82**

---

## Q4. Qdrant  
Now let's evaluate the following settings in Qdrant:

- `text = doc['question'] + ' ' + doc['text']`  
- `model_handle = "jinaai/jina-embeddings-v2-small-en"`  
- `limit = 5`

What's the MRR?

- 0.65  
- 0.75  
- 0.85  
- 0.95  

**Answer: 0.84**

---

## Q5. Cosine similarity  
We compute the average cosine similarity between LLM-generated answers and original answers.

What's the average cosine?

- 0.64  
- 0.74  
- 0.84  
- 0.94  

**Answer: 0.84**

---

## Q6. ROUGE  
Let's compute the average Rouge-1 F1 score across all answer pairs. What's the average?

- 0.25  
- 0.35  
- 0.45  
- 0.55  

**Answer: 0.35**

