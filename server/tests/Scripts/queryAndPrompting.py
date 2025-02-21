import os
import json
import pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq


model = SentenceTransformer('sentence-transformers/all-roberta-large-v1')
GROQ_API_KEY = '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'
groq_client = Groq(api_key=GROQ_API_KEY)

# Define index name
index_name = "surgery-steps"
pc = Pinecone(api_key='pcsk_4sW1a9_68r4WKSw9oZB8e3RQL6HCJ9EMF1m7bCUmEVDGyr3m36Xq3cGWtcCrpmt1pxrfix')

index = pc.Index(index_name)

# Hardcoded query
query_text = "How was the bone realigned during the surgery?"

# Create embedding for the query
query_embedding = model.encode(query_text).tolist()
search_response = index.query(vector = query_embedding, top_k=3, include_metadata=True)
# Constructing the prompt for Groq API
prompt = "You are an AI surgical assistant providing explanations for procedures. Below are relevant surgical steps:\n\n"
for match in search_response["matches"]:
    metadata = match["metadata"]
    prompt += f"Stage: {metadata['stage']}\nStep: {metadata['step_name']}\nDescription: {metadata['description']}\n\n"

prompt += f"\nQuestion: {query_text}\nAnswer:"

print("📜 Constructed Prompt for Groq API:\n", prompt)

# Query Groq API using their Python client
chat_completion = groq_client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.3-70b-versatile",
)

# Display Groq API response
groq_answer = chat_completion.choices[0].message.content
print("\n💡 Groq API Response:\n", groq_answer)

