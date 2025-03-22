'''
import requests
import json
import openai

# 设置OpenAI API密钥
openai.api_key = 'your-openai-api-key'

# 调用OpenAI GPT-3 API进行文本生成
def generate_text(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 可以选择其他模型，比如text-curie-001，text-ada-001等
            prompt=prompt,
            max_tokens=100,  # 设置最大字符数
            temperature=0.7  # 设置生成的随机性
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"


# 使用RunwayML API生成视频
def generate_video_from_text(text_prompt):
    api_url = "https://api.runwayml.com/v1/video/generate"
    headers = {
        "Authorization": "Bearer your-runwayml-api-key",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": text_prompt,
        "model": "runway-videogen",  # 选择你需要的视频生成模型
        "duration": 10,  # 设置视频长度（秒）
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 如果请求失败，会抛出异常
        video_url = response.json().get("video_url")
        return video_url
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
'''
from transformers import pipeline

def load_classifiers():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    scam_detector = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")
    return classifier, scam_detector
