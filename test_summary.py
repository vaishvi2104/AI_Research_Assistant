from services.summarizer import generate_summary

text = """
Artificial Intelligence (AI) is transforming industries across the world.
Machine Learning is a branch of AI that enables computers to learn from data.
Deep Learning uses neural networks with multiple layers and has applications
in computer vision, speech recognition, healthcare, robotics, and natural language processing.
Researchers continue to improve AI systems to make them more efficient and accurate.
"""

summary = generate_summary(text)

print("\n===== AI SUMMARY =====\n")
print(summary)