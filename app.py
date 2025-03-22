import streamlit as st
import openai
import os
import webbrowser


# 设置 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 页面设置
st.set_page_config(page_title="智识反诈", layout="centered")
st.title("🛡️ 智识反诈：老年人反诈骗辅助系统")

# 用户输入
text = st.text_area("📩 输入聊天记录或短信内容", height=150)

if text:
    with st.spinner("正在分析..."):
        try:
            # 调用 OpenAI API 进行情感分析
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Analyze the following text for emotions and detect if it's a scam: {text}",
                max_tokens=60,
                n=1,
                stop=None,
                temperature=0.5
            )
            result = response.choices[0].text.strip()

            if "fear" in result or "anger" in result or "disgust" in result:
                st.error(f"⚠️ 检测到可能的诈骗内容：{result}")

                # 调用 OpenAI API 进行诈骗类型识别
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Classify the following text into scam types: {text}",
                    max_tokens=60,
                    n=1,
                    stop=None,
                    temperature=0.5
                )
                scam_type = response.choices[0].text.strip()

                st.warning(f"🚨 疑似诈骗类型：{scam_type}")

                if st.button("📞 联系紧急联系人"):
                    st.success("已向紧急联系人发送提醒！")

                if st.button("📟 拨打110报警"):
                    webbrowser.open("tel:110")
            else:
                st.success("✅ 未检测到诈骗风险")
        except Exception as e:
            st.error(f"⚠️ 发生错误：{e}")

# 宣传图生成
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
