import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

# -----------------------------
# 頁面設定
# -----------------------------
st.set_page_config(page_title="旅遊Vlog問卷測驗", layout="centered")

st.title("🎬 旅遊 Vlog 內容風格與生活型態問卷")

# -----------------------------
# 問卷說明
# -----------------------------
st.markdown("""
您好：

感謝您撥冗填寫本問卷。本研究旨在探討不同生活型態的觀眾，
對旅遊 Vlog 影片內容形式及 YouTuber 個人特質的偏好差異。

本問卷採匿名填答方式，所有資料僅供學術研究使用，
不涉及任何商業用途。請您依個人真實想法作答，
內容無對錯之分，敬請放心填寫。

填答流程包含生活型態測驗與影片觀賞，
系統將分配兩支旅遊 Vlog 影片，請您觀看後依題項作答即可。

若您對本研究有任何疑問，歡迎與研究者聯繫：  
中國文化大學新聞學系研究生 **許秋琳**  
📧 電子郵件：**xql0234@gmail.com**

再次感謝您的協助！
""")

st.write("---")

# -----------------------------
# 第一部分：基本資料
# -----------------------------
st.header("第一部分：基本資料")

watch_vlog = st.radio("1. 過去一個月是否看過「旅遊相關」YouTube影片？", ["是", "否"])
if watch_vlog == "否":
    st.info("感謝您的參與，本問卷到此結束 🙏")
    st.stop()

watch_freq = st.radio("2. 您每周平均觀看旅遊Vlog次數為：", ["1~3次", "4~6次", "7~9次", "10次以上"])
watch_time = st.radio("3. 您每次平均觀看旅遊Vlog所花費的時間為：", ["15分鐘以下", "15~30分鐘", "30~45分鐘", "45分鐘以上"])
gender = st.radio("4. 您的生理性別：", ["男", "女"])
age_group = st.radio("5. 您的年齡：", ["15~19歲", "20~29歲", "30~39歲", "40~49歲", "50~59歲", "60歲以上"])
edu = st.radio("6. 您現階段最高的教育程度：", ["國中(含)以下", "高中(職)", "大學(專)", "研究所(含)以上"])
job = st.selectbox("7. 您的職業：", [
    "農林漁牧礦業", "製造業", "服務業", "自由業", "商業", "電子資訊工程業", "專業人員(法律、醫療、藝術表演等)",
    "軍、警、公、教", "家管", "學生", "退休/待業中/無業", "其他"
])
income = st.selectbox("8. 您的每月可支配所得：", [
    "20,000元以下", "20,001~40,000元", "40,001~60,000元", "60,001~80,000元",
    "80,001~100,000元", "100,001~120,000元", "120,001~140,000元", "140,001~160,000元",
    "160,001~180,000元", "180,001~200,000元", "200,001元以上"
])

# -----------------------------
# 第二部分：生活型態測驗
# -----------------------------
st.header("第二部分：生活型態")

questions = {
    "探索冒險型": [
        "我喜歡嘗試新地方與不熟悉的活動。",
        "我會期待生活中有些驚喜。",
        "我不喜歡太有規律的生活。",
        "我享受具挑戰性的旅遊體驗。"
    ],
    "社交分享型": [
        "我喜歡在社群媒體上分享我的旅遊經驗或照片。",
        "我會透過社群平台追蹤旅遊YouTuber。",
        "我參加旅遊活動是為了聯絡鄰居或朋友之間的感情。",
        "我常與朋友討論旅遊 Vlog 的內容，或交換旅遊資訊。"
    ],
    "休閒放鬆型": [
        "我平常喜歡和朋友一起到戶外打球、逛街或是到郊外踏青。",
        "我經常安排兩、三天以上的旅遊。",
        "旅遊是我最喜歡的休閒活動。",
        "我看旅遊Vlog多半為了紓壓。"
    ],
    "理性規劃型": [
        "我習慣比較價格、評估性價比後再決定。",
        "我會做完整行前功課與時間規畫。",
        "我在旅行時較少依靠隨興或臨時決定。",
        "我會定期搜尋旅遊相關資訊。"
    ]
}

responses = {}
question_num = 1
for category, qs in questions.items():
    for q in qs:
        question_label = f"{question_num}. {q}"
        responses[q] = st.slider(question_label, 1, 7, 4, key=q)
        question_num += 1

# -----------------------------
# 影片連結設定
# -----------------------------
videos = {
    "探索冒險型": "https://www.youtube.com/watch?v=rn3vkZf1NEw",
    "社交分享型": "https://www.youtube.com/watch?v=H_OVtdOKu8g",
    "休閒放鬆型": "https://www.youtube.com/watch?v=xb8Va3qr62k",
    "理性規劃型": "https://www.youtube.com/watch?v=LpFSGtGw4X8"
}

# -----------------------------
# 第三部分：影片評價題項
# -----------------------------
video_questions = [
    "旅遊Vlog中的畫面呈現與拍攝手法提升了我對旅遊地點的臨場感。",
    "旅遊Vlog的剪輯方式讓我覺得流暢自然。",
    "我偏好畫質高、攝影技術佳的旅遊Vlog。",
    "旅遊Vlog提供的旅遊資訊（行程、交通、住宿、預算等）對我很有幫助。",
    "影片提供的資訊、實務建議比旅遊書或一般官方資訊更貼近實際情況。",
    "我能從這支旅遊Vlog中獲得旅程規劃的靈感。",
    "影片的節奏與情緒鋪陳能吸引我持續觀看。",
    "創作者在影片中的表達方式（如口語敘述、旁白或情感分享）能讓我投入其中。",
    "影片中創作者的旅程經歷與心境變化，讓我感到共鳴。",
    "觀看完此影片能讓我感到愉快、放鬆。",
    "影片中的趣味設計能讓我持續想看下去",
    "觀看完影片會讓我更想去旅行。"
]

youtuber_questions = [
    "我可以信任這位YouTuber所提供的旅遊資訊。",
    "我覺得這位YouTuber的形象是正面的。",
    "我認為這位YouTuber對旅遊相關知識很熟悉。",
    "這位YouTuber提供的建議具專業判斷或經驗累積。",
    "我認為這位YouTuber的外型是具有吸引力的。",
    "我覺得這位YouTuber具有個人特色、風格鮮明。",
    "我認為可以透過旅遊Vlog了解這位YouTuber。",
    "這位YouTube不時會分享個人喜好或提到過去的生活經歷。。",
]

# -----------------------------
# 提交與結果計算
# -----------------------------
if st.button("提交生活型態測驗"):
    category_scores = {cat: sum(responses[q] for q in qs) for cat, qs in questions.items()}
    lifestyle = max(category_scores, key=category_scores.get)
    matched_video = videos[lifestyle]
    other_videos = [v for k, v in videos.items() if k != lifestyle]
    random_video = random.choice(other_videos)

    st.success(f"你的生活型態為：**{lifestyle}** 🎉")

    # 第一支影片
    st.markdown("### 📺 第一支影片")
    st.video(matched_video)
    st.write("請觀看影片後回答以下題目：")

    matched_scores = {}
    for i, q in enumerate(video_questions + youtuber_questions, start=10):
        matched_scores[f"影片1_Q{i}"] = st.slider(f"{i}. {q}", 1, 7, 4, key=f"mv1_{i}")

    st.markdown("---")

    # 第二支影片
    st.markdown("### 🎬 第二支影片")
    st.video(random_video)
    st.write("請觀看影片後回答以下題目：")

    random_scores = {}
    for i, q in enumerate(video_questions + youtuber_questions, start=10):
        random_scores[f"影片2_Q{i}"] = st.slider(f"{i}. {q}", 1, 7, 4, key=f"mv2_{i}")

    if st.button("提交整份問卷"):
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "觀看旅遊Vlog": watch_vlog,
            "觀看頻率": watch_freq,
            "觀看時間": watch_time,
            "性別": gender,
            "年齡": age_group,
            "教育程度": edu,
            "職業": job,
            "月可支配所得": income,
            "生活型態": lifestyle,
            **category_scores,
            "matched_video": matched_video,
            "random_video": random_video,
            **matched_scores,
            **random_scores
        }

        df = pd.DataFrame([data])
        file_path = "responses.csv"
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
        else:
            df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")

        st.success("✅ 問卷結果已記錄，感謝您的參與！")


