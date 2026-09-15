"""
Trash to Treasure - Web UI
Run with: streamlit run app.py
"""

import streamlit as st
from trash_treasure import TrashTreasureAssistant

st.set_page_config(page_title="Trash to Treasure", page_icon="\u267b\ufe0f")
st.title("\u267b\ufe0f Trash to Treasure")
st.caption("Enter an unwanted item and get reuse, recycling, and DIY ideas.")

# Offline icon-style visuals -- no internet needed, matched by keywords
# found in the category text. This avoids depending on external images
# loading correctly during a live demo.
ICON_MAP = [
    ("battery", "\U0001F50B"),
    ("hazardous", "\u26A0\uFE0F"),
    ("plastic", "\U0001F9F4"),
    ("paper", "\U0001F4C4"),
    ("cardboard", "\U0001F4E6"),
    ("glass", "\U0001F37E"),
    ("metal", "\U0001F96B"),
    ("ceramic", "\U0001F3FA"),
    ("electronics", "\U0001F4F1"),
    ("foam", "\U0001F4E6"),
    ("wax", "\U0001F56F\uFE0F"),
    ("organic", "\U0001F342"),
    ("liquid", "\U0001FAD9"),
    ("rubber", "\U0001F6DE"),
    ("wood", "\U0001FAB5"),
    ("fabric", "\U0001F455"),
    ("cork", "\U0001F377"),
]


def get_icon(category: str) -> str:
    cat_lower = category.lower()
    for keyword, icon in ICON_MAP:
        if keyword in cat_lower:
            return icon
    return "\u267B\uFE0F"  # default recycling symbol


@st.cache_resource
def load_assistant():
    return TrashTreasureAssistant()


assistant = load_assistant()

user_item = st.text_input(
    "What unwanted item do you have?",
    placeholder="e.g. plastic bottle, old t-shirt, tin can",
)

if user_item:
    result = assistant.get_ideas(user_item)

    if result is None:
        st.warning(
            "I don't have specific ideas for that item yet. "
            "Try: plastic bottle, newspaper, old t-shirt, cardboard box, "
            "glass jar, tin can, old smartphone, egg carton, wine cork, old book."
        )
    else:
        icon = get_icon(result["category"])

        # Large icon-style visual header, no internet needed
        st.markdown(
            f"<div style='font-size:64px; text-align:center;'>{icon}</div>",
            unsafe_allow_html=True,
        )
        st.subheader(f"{result['matched_item'].title()} \u2014 {result['category']}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**\U0001F501 Reuse Idea**")
            st.write(result["reuse_ideas"])
            st.markdown("**\u2705 Recycling**")
            st.write(result["recycling_suggestions"])
        with col2:
            st.markdown("**\U0001F6E0\uFE0F DIY Idea**")
            st.write(result["diy_ideas"])
            st.markdown("**\U0001F30D Did You Know?**")
            st.write(result["environmental_tip"])

        # Copy/share: Streamlit's st.code() block renders a built-in
        # copy icon in the top-right corner automatically -- no extra
        # library needed.
        st.markdown("**\U0001F4CB Copy this result**")
        share_text = (
            f"Item: {result['matched_item'].title()} ({result['category']})\n"
            f"Reuse Idea: {result['reuse_ideas']}\n"
            f"Recycling: {result['recycling_suggestions']}\n"
            f"DIY Idea: {result['diy_ideas']}\n"
            f"Did You Know: {result['environmental_tip']}"
        )
        st.code(share_text, language=None)
