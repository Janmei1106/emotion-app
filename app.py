import streamlit as st
import pandas as pd

st.set_page_config(page_title="情緒歌曲 App", page_icon="🎵", layout="wide")

# 頁面選單
menu = st.sidebar.radio("📁 選單", ["首頁", "情緒探索"])

@st.cache_data
def load_excel(file):
    df = pd.read_excel(file)
    df = df.assign(情緒=df['情緒'].str.split('、')).explode('情緒')
    df = df.assign(情境=df['情境'].str.split('、')).explode('情境')
    df['情緒'] = df['情緒'].str.strip()
    df['情境'] = df['情境'].str.strip()
    return df

# -----------------------------------
# 首頁畫面
# -----------------------------------
if menu == "首頁":
    st.title("🎶 歡迎來到情緒歌曲 App")

    st.subheader("🌐 請選擇語言")
    langs = ["華語", "英語", "日語", "韓語"]
    lang_cols = st.columns(len(langs))
    for i, lang in enumerate(langs):
        lang_cols[i].button(lang)

    st.subheader("🎭 入門情緒")
    moods = ["開心", "難過", "戀愛", "思念", "遺憾", "心痛"]
    mood_cols = st.columns(len(moods))
    for i, mood in enumerate(moods):
        mood_cols[i].button(mood)

# -----------------------------------
# 情緒探索畫面
# -----------------------------------
elif menu == "情緒探索":
    st.title("🔍 情緒探索")

    uploaded_file = st.file_uploader("請上傳 Excel（需含：歌名、歌手、情緒、情境、YouTube 連結...）", type="xlsx")
    
    if uploaded_file:
        try:
            df_exp = load_excel(uploaded_file)
            st.success("✅ 成功載入！")

            all_emotions = sorted(df_exp['情緒'].dropna().unique())
            if 'chosen_emotion' not in st.session_state:
                st.session_state.chosen_emotion = all_emotions[0]

            st.sidebar.subheader("🎭 選擇情緒")
            for i in range(0, len(all_emotions), 2):
                cols = st.sidebar.columns(2)
                for j in range(2):
                    if i + j < len(all_emotions):
                        emo = all_emotions[i + j]
                        if cols[j].button(emo, key=f"emo_{emo}"):
                            st.session_state.chosen_emotion = emo

            emotion = st.session_state.chosen_emotion
            scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].dropna().unique()
            scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))

            st.subheader("🎧 搜尋結果")
            result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)]

            if result.empty:
                st.warning("😢 找不到符合的歌曲")
            else:
                for _, row in result.iterrows():
                    st.markdown("---")
                    st.markdown(f"### 🎵 {row['歌名']} - {row['歌手']}")
                    st.markdown(f"📌 情緒：`{row['情緒']}` ｜ 情境：`{row['情境']}`")
                    st.markdown(f"▶️ [前往 YouTube]({row['YouTube 連結']})")

                    if '圖片連結' in row and pd.notna(row['圖片連結']):
                        st.image(row['圖片連結'], width=400)

                    if '歌詞' in row and pd.notna(row['歌詞']):
                        with st.expander("📝 歌詞"):
                            st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
