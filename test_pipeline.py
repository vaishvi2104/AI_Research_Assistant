from transformers import pipeline

summarizer = pipeline("summarization")

print("Pipeline loaded successfully!")