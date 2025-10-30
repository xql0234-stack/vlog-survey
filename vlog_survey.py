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
st.write("請根據您的想法回答以下題目，1 表示『非常不同意』，5 表示『非常同意』。")

# -----------------------------
# 基本資料區
# -----------------------------
st.header("👤 基本資料")
name = st.text_input("您的姓名（可留空）")
age = st.number_input("年齡", min_value=10, max_value=100, step=1)
gender = st.radio("性別", ["男", "女", "其他"], index=0)

# -----------------------------
# 題目分類
# -----------------------------
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

# -----------------------------
# 影片連結
# -----------------------------
videos = {
    "探索冒險型": "https://www.youtube.com/watch?v=rn3vkZf1NEw&list=PLaTgGdKCl5EgUqoegkfpAAqW0U3VtIaor&index=4",
    "社交分享型": "https://www.youtube.com/watch?v=H_OVtdOKu8g&list=PLaTgGdKCl5EgUqoegkfpAAqW0U3VtIaor&index=2",
    "休閒放鬆型": "https://www.youtube.com/watch?v=oMnOt9v3YSw&list=PLaTgGdKCl5EgUqoegkfpAAqW0U3VtIaor&index=3",
    "理性規劃型": "https://www.youtube.com/watch?v=LpFSGtGw4X8&list=PLaTgGdKCl5EgUqoegkfpAAqW0U3VtIaor"
}

# -----------------------------
# 問卷輸入區
# -----------------------------
st.header("📋 問卷內容")
responses = {}
for category, qs in questions.items():
    st.subheader(category)
    for q in qs:
        responses[q] = st.slider(q, 1, 5, 3, key=q)

# -----------------------------
# 提交與結果計算
# -----------------------------
if st.button("提交問卷"):
    # 計算每類分數
    category_scores = {}
    for cat, qs in questions.items():
        category_scores[cat] = sum(responses[q] for q in qs)

    # 判定生活型態
    lifestyle = max(category_scores, key=category_scores.get)
    st.success(f"你的生活型態為：**{lifestyle}** 🎉")

    # 配對影片與隨機影片
    matched_video = videos[lifestyle]
    other_videos = [v for k, v in videos.items() if k != lifestyle]
    random_video = random.choice(other_videos)

    st.write("📺 以下是為你推薦的兩支影片：")
    st.markdown(f"**配對影片（{lifestyle}）**")
    st.video(matched_video)
    st.markdown("**隨機影片**")
    st.video(random_video)

    # -----------------------------
    # 儲存結果
    # -----------------------------
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "姓名": name,
        "年齡": age,
        "性別": gender,
        "生活型態": lifestyle,
        "score_探索冒險型": category_scores["探索冒險型"],
        "score_社交分享型": category_scores["社交分享型"],
        "score_休閒放鬆型": category_scores["休閒放鬆型"],
        "score_理性規劃型": category_scores["理性規劃型"],
        "matched_video": matched_video,
        "random_video": random_video
    }

    df = pd.DataFrame([data])
    file_path = "responses.csv"

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")

    st.info("✅ 問卷結果已記錄，感謝您的參與！")
