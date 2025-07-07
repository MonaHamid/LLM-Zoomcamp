# From REST to Reasoning: Ingest, Index, and Query with dlt and Cognee

**Video**: [https://www.youtube.com/watch?v=MNt_KK32gys](https://www.youtube.com/watch?v=MNt_KK32gys)

---

## 📝 Homework Submission

### ✅ Question 1. dlt Version
**Question**: What's the version of dlt that you installed?

**Answer**: `1.12.3`  
*(Or replace with the exact version printed from `print(dlt.__version__)`)*

---

### ✅ Question 2. dlt pipeline
**Question**: How many rows were inserted into the `zoomcamp_data` collection?

**Answer**: `948 rows`  
*(Based on the output: `- zoomcamp_data: 948 row(s)`)*

---

### ✅ Question 3. Embeddings
**Question**: When inserting the data, an embedding model was used. Which one?

**Answer**: `fast-bge-small-en`  
*(As found in `db.qdrant/meta.json` under the embedding model info)*

---

## 💡 Notes
- Used `@dlt.resource` to wrap the `zoomcamp_data()` generator
- Qdrant folder created locally as `db.qdrant`
- Embedding model automatically selected via `qdrant-client[fastembed]`

---

Prepared by: *Fareeda*  


