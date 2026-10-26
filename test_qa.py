from services.qa_service import ask_question

sample_paper_text = """Title: Attention Is All You Need.
Authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin.

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism.

The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU, ByteNet and ConvS2S.

The Transformer follows an overall architecture using stacked self-attention and point-wise, fully connected layers. For the base model, we use 6 encoder layers and 6 decoder layers with a model dimension of d_model = 512. Multi-head attention allows the model to jointly attend to information from different representation subspaces. We use 8 parallel attention heads for the base model.

We trained our models on 8 NVIDIA P100 GPUs. For base models, each training step took about 0.4 seconds. We trained the base models for a total of 100,000 steps or 12 hours. The Adam optimizer was employed with beta1 = 0.9, beta2 = 0.98 and epsilon = 1e-9.

On the WMT 2014 English-to-German translation task, the big transformer model achieves a state-of-the-art BLEU score of 28.4. On the WMT 2014 English-to-French translation task, our model establishes a new BLEU score of 41.8.

In this work, we presented the Transformer, the first sequence transduction model based entirely on attention."""

questions = [
    "Who are the authors of Attention Is All You Need?",
    "How many parallel attention heads are used for the base model?",
    "Which GPUs were used for training?",
    "What BLEU score was achieved on English-to-German translation?",
    "What optimizer was employed during training?"
]

print("\n==========================================")
print("  TESTING HYBRID RAG QA ENGINE")
print("==========================================\n")

for q in questions:
    result = ask_question(q, sample_paper_text)
    print(f"[*] Question: {q}")
    print(f"[-] Direct Answer: {result['answer']}")
    print(f"[-] Confidence: {result.get('confidence')}")
    print(f"[-] Evidence: {result.get('context')}")
    print("-" * 50)