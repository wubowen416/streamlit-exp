import numpy as np
import streamlit as st

# np.random.seed(1234)


def get_url(idx: str, name: str):
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2026-robot-facial-mimicry/{name}/{idx}.png"
    return url


def get_neutral_url():
    url = f"https://wu-cloud-bucket.s3.ap-northeast-3.amazonaws.com/2026-robot-facial-mimicry/robot_neutral.png"
    return url


if "samples" not in st.session_state:
    idcs = [
        102,
        303,
        439,
        845,
        1359,
        1485,
        1638,
        1667,
        1713,
        1790,
        # 1992,
        # 2012,
        # 2119,
        # 3485,
        # 3713,
        # 3766,
        # 3773,
        # 3876,
        # 5087,
        # 5122,
    ]
    samples = []
    for idx in idcs:
        for name in [
            "fim_mp",
            "gpt4o_const",
            "gpt5.2_const",
            "gpt5.2_iprop%2B",
            "neutral",
        ]:
            samples.append(
                {
                    "url_t": get_url(str(idx), "target"),
                    "url_r": (
                        get_neutral_url()
                        if name == "neutral"
                        else get_url(str(idx), name)
                    ),
                    "model_name": name,
                    "idx": idx,
                }
            )
    np.random.shuffle(samples)
    st.session_state["samples"] = samples
if "num_samples" not in st.session_state:
    st.session_state["num_samples"] = len(st.session_state["samples"])
if "sample_idx" not in st.session_state:
    st.session_state["sample_idx"] = 0


def choice_to_value(choice: str) -> int:
    match choice:
        case "1":
            value = 1
        case "2":
            value = 2
        case "3":
            value = 3
        case "4":
            value = 4
        case "5":
            value = 5
        case "6":
            value = 6
        case "7":
            value = 7
    return value


def on_form_submitted():
    # Record choice
    similarity_value = choice_to_value(
        st.session_state[f'similarity_choice_{st.session_state["sample_idx"]}']
    )
    naturalness_value = choice_to_value(
        st.session_state[f'naturalness_choice_{st.session_state["sample_idx"]}']
    )

    st.session_state["samples"][st.session_state["sample_idx"]][
        "similarity"
    ] = similarity_value
    st.session_state["samples"][st.session_state["sample_idx"]][
        "naturalness"
    ] = naturalness_value

    # Move to next pair
    st.session_state["sample_idx"] += 1


# Interface
st.title("実験")
st.warning(
    "ページを更新したりタブを閉じたりしないでください。入力済みのデータが失われます。"
)
progress_bar_text = "進捗"
progress_bar = st.progress(
    0, text=f"{progress_bar_text}: {0}/{st.session_state['num_samples']}"
)


@st.fragment
def exp_fragment():
    # Check if all completed
    if st.session_state["sample_idx"] == st.session_state["num_samples"]:
        st.session_state["log"] = {"samples": st.session_state["samples"]}

        # Move to next
        st.switch_page("pages/comment.py")

    # Get sample info
    sample = st.session_state["samples"][st.session_state["sample_idx"]]

    # Place interface
    with st.container(border=True):
        st.subheader(f"以下の画像を見て、質問にお答えください。")
        col1, col2 = st.columns([1, 1], border=True)
        with col1:
            st.subheader("ロボットの表情", divider="gray")
            st.image(sample["url_r"])
        with col2:
            st.subheader("人間の表情", divider="gray")
            st.image(sample["url_t"])
        # st.write(sample["idx"])

        naturalness_choice = st.radio(
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
            key=f'naturalness_choice_{st.session_state["sample_idx"]}',
        )
        similarity_choice = st.radio(
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
            key=f'similarity_choice_{st.session_state["sample_idx"]}',
        )
        choice_has_not_been_made = (
            similarity_choice == None or naturalness_choice == None
        )
        st.button(
            "次へ",
            on_click=on_form_submitted,
            disabled=choice_has_not_been_made,
            help="質問にお答えください。" if choice_has_not_been_made else "",
        )

    progress_bar.progress(
        st.session_state["sample_idx"] / st.session_state["num_samples"],
        f"{progress_bar_text}: {st.session_state['sample_idx']}/{st.session_state['num_samples']}",
    )


exp_fragment()
