import streamlit as st
from transformers import pipeline
import openai
import webbrowser
import os

# 从环境变量中读取 API 密钥
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="智识反诈", layout="centered")

# 初始化模型
st.title("🛡️ 智识反诈：老年人反诈骗辅助系统")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
scam_detector = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

# 用户输入
text = st.text_area("📩 输入聊天记录或短信内容", height=150)

if text:
    with st.spinner("正在分析..."):
        try:
            pred = scam_detector(text)[0]
            label = pred['label']
            score = pred['score']
            if score > 0.8 and label in ['anger', 'fear']:
                st.error(f"⚠️ 检测到可能的诈骗内容（置信度：{score:.2f}）")
                scam_type = classifier(text, ["网络购物诈骗", "虚假中奖诈骗", "假冒亲属", "投资理财诈骗"])["labels"][0]
                st.warning(f"🚨 疑似诈骗类型：{scam_type}")
                if st.button("📞 联系紧急联系人"):
                    st.success("已向紧急联系人发送提醒！")
                if st.button("📟 拨打110报警"):
                    webbrowser.open("tel:110")  # 模拟拨打
            else:
                st.success("✅ 未检测到诈骗风险")
        except Exception as e:
            st.error(f"⚠️ 发生错误：{e}")

# 生成反诈骗宣传图
st.subheader("🎨 生成反诈骗宣传图")

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']

if st.button("生成反诈海报"):
    img_url = generate_image("老年人防范电信诈骗的宣传海报")
    st.image(img_url, caption="生成的反诈骗宣传图")

# 模拟支付拦截
st.subheader("🛑 支付风险拦截模拟")
if st.button("模拟访问支付页面"):
    st.warning("⚠️ 支付页面访问被拦截，因检测到诈骗风险。")
