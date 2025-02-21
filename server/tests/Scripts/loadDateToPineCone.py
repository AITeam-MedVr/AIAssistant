import os
import json
import pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key='pcsk_4sW1a9_68r4WKSw9oZB8e3RQL6HCJ9EMF1m7bCUmEVDGyr3m36Xq3cGWtcCrpmt1pxrfix')

# Define index name
index_name = "surgery-steps"

# Check if index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,  # Ensure this matches your embedding model output
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Index '{index_name}' created successfully.")

# Connect to the existing index
index = pc.Index(index_name)

print(f"Connected to Pinecone index: {index_name}")

# Load Sentence Transformer model
model = SentenceTransformer('sentence-transformers/all-roberta-large-v1')

# Function to read JSON data
def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Function to process and upsert data into Pinecone
def upsert_data_from_json(json_data):
    formatted_vectors = []

    for stage in json_data["stages"]:
        for i, step in enumerate(stage["steps"]):
            prev_step_desc = stage["steps"][i - 1]["description"] if i > 0 else ""
            next_step_desc = stage["steps"][i + 1]["description"] if i < len(stage["steps"]) - 1 else ""

            # ✅ Ensure metadata values are never `None`
            metadata = {
                "stage": stage["stage"],
                "step_name": step["step_name"],
                "description": step["description"],
                "prev_step_desc": prev_step_desc if prev_step_desc else "",
                "next_step_desc": next_step_desc if next_step_desc else "",
                "tool_used": step.get("tool_used", ""),
                "anatomy_targeted": step.get("anatomy_targeted", "")
            }

            # Create embedding for the step
            text = f"Stage: {stage['stage']}\nStep: {step['step_name']}\nDescription: {step['description']}\nPrevious: {prev_step_desc}\nNext: {next_step_desc}"
            embedding = model.encode(text).tolist()

            formatted_vectors.append({
                "id": step["step_id"],
                "values": embedding,
                "metadata": metadata
            })

    # ✅ Upsert data into Pinecone
    index.upsert(vectors=formatted_vectors)
    print(f"✅ Successfully upserted {len(formatted_vectors)} steps into Pinecone.")

# Load JSON file
json_filepath = "surgery_data.json"  # Update with your JSON file path
surgery_data = load_json(json_filepath)

# Upsert into Pinecone
upsert_data_from_json(surgery_data)