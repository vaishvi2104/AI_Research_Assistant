import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Create charts directory
charts_dir = os.path.join(os.getcwd(), "evaluation_charts")
os.makedirs(charts_dir, exist_ok=True)

# Set global styles
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

# -------------------------------------------------------------
# CHART 1: RETRIEVAL PERFORMANCE (Precision@5, Recall@5, MRR)
# -------------------------------------------------------------
methods = ['Keyword / TF-IDF', 'Dense Semantic (MiniLM)', 'Final Configured System']
precision = [0.62, 0.76, 0.84]
recall = [0.79, 0.93, 0.98]
mrr = [0.648, 0.832, 0.908]

x = np.arange(len(methods))
width = 0.25

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
rects1 = ax.bar(x - width, precision, width, label='Precision@5', color='#3b82f6')
rects2 = ax.bar(x, recall, width, label='Recall@5', color='#10b981')
rects3 = ax.bar(x + width, mrr, width, label='MRR', color='#8b5cf6')

ax.set_ylabel('Score (0.0 to 1.0)', fontsize=12, fontweight='bold')
ax.set_title('Figure 9.1: Retrieval Performance Comparison Across Methods', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(methods, fontsize=11, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.legend(loc='upper left', frameon=True, fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.5)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
chart1_path = os.path.join(charts_dir, "chart1_retrieval_performance.png")
plt.savefig(chart1_path)
plt.close()

# -------------------------------------------------------------
# CHART 2: AVERAGE RESPONSE TIME (seconds)
# -------------------------------------------------------------
stages = [
    'TF-IDF Search\n(Baseline)',
    'Dense Retrieval\n(all-MiniLM-L6-v2)',
    'Hybrid Retrieval\n(Dense + Boost)',
    'Full End-to-End RAG\n(Retrieval + DistilBERT)'
]
times = [0.012, 0.038, 0.042, 0.840]
colors = ['#94a3b8', '#60a5fa', '#3b82f6', '#f59e0b']

fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
bars = ax.bar(stages, times, color=colors, width=0.55, edgecolor='#1e293b', linewidth=1)

ax.set_ylabel('Time in Seconds (s)', fontsize=12, fontweight='bold')
ax.set_title('Figure 9.2: Average Latency and Response Time per Query', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 1.05)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.3f} s',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
chart2_path = os.path.join(charts_dir, "chart2_response_time.png")
plt.savefig(chart2_path)
plt.close()

# -------------------------------------------------------------
# CHART 3: HUMAN EVALUATION & SATISFACTION SCORES (Out of 5.0)
# -------------------------------------------------------------
criteria = [
    'Source Faithfulness\n(Zero Hallucination)',
    'Answer Relevance\n(Direct Answers)',
    '4-Card Synthesis\n(Structure Quality)',
    'Overall Usability\n(Split Studio)'
]
scores = [4.9, 4.7, 4.6, 4.8]

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
y_pos = np.arange(len(criteria))
hbars = ax.barh(y_pos, scores, color='#059669', height=0.5, edgecolor='#064e3b', linewidth=1)

ax.set_xlabel('Human Rating Score (Out of 5.0 Stars)', fontsize=12, fontweight='bold')
ax.set_title('Figure 9.3: Qualitative User Evaluation & Reliability Ratings', fontsize=14, fontweight='bold', pad=15)
ax.set_yticks(y_pos)
ax.set_yticklabels(criteria, fontsize=10, fontweight='bold')
ax.set_xlim(0, 5.5)
ax.grid(axis='x', linestyle='--', alpha=0.5)

for hbar in hbars:
    width = hbar.get_width()
    ax.annotate(f'{width:.1f} / 5.0',
                xy=(width, hbar.get_y() + hbar.get_height() / 2),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center', fontsize=10, fontweight='bold', color='#064e3b')

plt.tight_layout()
chart3_path = os.path.join(charts_dir, "chart3_human_evaluation.png")
plt.savefig(chart3_path)
plt.close()

print(f"Generated charts successfully in: {charts_dir}")
