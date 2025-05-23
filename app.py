import streamlit as st
import pandas as pd

st.set_page_config(page_title="情緒歌曲 App", page_icon="🎵", layout="wide")
st.title("🎶 情境音樂探索 App")

# 側邊上傳與頁面選擇
uploaded_file = st.sidebar.file_uploader("📁 上傳歌曲 Excel（欄位：歌名、歌手、情境、語言、點閱率...）", type="xlsx")
menu = st.sidebar.radio("📂 頁面", ["首頁", "情境探索"])

@st.cache_data
def load_excel(file):
    df = pd.read_excel(file)
    df['情境'] = df['情境'].str.strip()
    df['語言'] = df['語言'].str.strip()
    return df

# 若已上傳檔案
if uploaded_file:
    try:
        df = load_excel(uploaded_file)

        # 🏠 首頁
        if menu == "首頁":
            st.subheader("🌐 請選擇語言")
            langs = sorted(df['語言'].dropna().unique())
            lang_cols = st.columns(len(langs))
            for i, lang in enumerate(langs):
                lang_cols[i].button(lang)

            st.subheader("🔥 點閱率排行榜 Top 5")
            top5 = df.sort_values("點閱率", ascending=False).head(5)
            for _, row in top5.iterrows():
                st.markdown(f"**🎵 {row['歌名']} - {row['歌手']}**")
                st.markdown(f"📌 語言：`{row['語言']}` ｜ 🔥 點閱率：{row['點閱率']}")
                st.markdown(f"[▶️ 前往收聽]({row['YouTube 連結']})")
                st.markdown("---")

        # 🎭 情境探索
        elif menu == "情境探索":
            st.subheader("🎭 情境分類探索")
            all_scenes = sorted(df['情境'].dropna().unique())
            all_langs = sorted(df['語言'].dropna().unique())

            # 選擇語言
            lang = st.sidebar.selectbox("🌐 篩選語言", ["全部"] + all_langs)

            # 選擇情境
            st.sidebar.subheader("🎬 請選擇情境")
            if 'chosen_scene' not in st.session_state:
                st.session_state.chosen_scene = all_scenes[0]

            for i in range(0, len(all_scenes), 2):
                cols = st.sidebar.columns(2)
                for j in range(2):
                    if i + j < len(all_scenes):
                        scene = all_scenes[i + j]
                        if cols[j].button(scene, key=f"scene_{scene}"):
                            st.session_state.chosen_scene = scene

            chosen_scene = st.session_state.chosen_scene

            # 過濾資料
            result = df[df['情境'] == chosen_scene]
            if lang != "全部":
                result = result[result['語言'] == lang]

            st.subheader(f"🔍 結果：情境 = `{chosen_scene}`，語言 = `{lang}`")
            if result.empty:
                st.warning("😢 找不到符合的歌曲")
            else:
                for _, row in result.iterrows():
                    st.markdown("---")
                    st.markdown(f"### 🎵 {row['歌名']} - {row['歌手']}")
                    st.markdown(
                        f"🎬 情境：`{row['情境']}` ｜ 🌐 語言：`{row['語言']}` ｜ 🔥 點閱率：{row['點閱率']}"
                    )
                    if '圖片連結' in row and pd.notna(row['圖片連結']):
                        st.image(row['圖片連結'], width=400)
                    st.markdown(f"[▶️ YouTube 連結]({row['YouTube 連結']})")
                    if '歌詞' in row and pd.notna(row['歌詞']):
                        with st.expander("📝 查看歌詞"):
                            st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")

else:
    st.warning("📥 請先上傳符合欄位格式的 Excel 檔才能使用本系統！")
