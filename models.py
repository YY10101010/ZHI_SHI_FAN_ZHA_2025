from transformers import pipeline

def load_classifiers():
    # 更轻量的零样本分类模型
    classifier = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    )

    # 更适合情绪分析的模型
    scam_detector = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=1
    )

    return classifier, scam_detector
