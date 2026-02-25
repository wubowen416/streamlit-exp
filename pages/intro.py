import streamlit as st

st.title("実験内容")

with st.container(border=True):
    st.header("実験説明")
    st.markdown(
        """
        本実験では、ロボットが人の表情を模倣しています。
        ロボットの表情と人間の表情の写真を見て、以下の2点について印象評価をしていただきます。
        - **自然さ**：ロボットの表情は、自然な表情であるか？
        - **類似度**：ロボットの表情は、人間の表情と似ているか？顔の形態ではなく、表情の内容について比較してください。
        
        各質問にはラジオボタン式の選択肢があります。もっとも当てはまるものを選択してください。

        合計50セットを評価していただきます。所要時間は30分程度です。

        画面が大きすぎる、または小さすぎる場合は、ブラウザのズーム機能（Ctrl/CMD＋「+」「-」キー）で調整が可能です。
        """
    )

    st.header("実験ページの例")
    st.markdown(
        """
        実験のページは以下のように表示されます。
        """
    )

    with st.container(border=True):
        st.subheader(f"以下の画像を見て、質問にお答えください。")
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("ロボットの表情", divider="gray")
            st.image(
                "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250921-robot-facial-mimicry-with-vlm-pre-exp/face_001/robot_frame_fim_vlm.png"
            )
        with col2:
            st.subheader("人間の表情", divider="gray")
            st.image(
                "https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/250921-robot-facial-mimicry-with-vlm-pre-exp/face_001/target_frame.png"
            )
        st.radio(
            "Q1: ロボットの表情の**自然さ**はいかがですか？\n\n1:不自然、4:どちらとも言えない、7:自然",
            options=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
            ],
            index=None,
            horizontal=True,
        )
        st.radio(
            "Q2: ロボットは、どれくらい人間の表情を**模倣できた**と思いますか？\n\n1:できなかった、4:ある程度できた、7:できた",
            options=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
            ],
            index=None,
            horizontal=True,
        )

    st.warning(
        "回答の仕方が明らかに不誠実と判断される場合は、報酬をお支払いできないことがあります。問題文をよく読み、ご理解いただいた上でご回答ください。"
    )

next_button = st.button(label="実験へ")
if next_button:
    st.switch_page("pages/exp.py")
