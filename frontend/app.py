import streamlit as st
import requests

st.title("🛡️ Cybersecurity AI Agent Dashboard")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input.strip():
        try:
            response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
            data = response.json()
            reply = data.get("reply", "No reply")
            detections = data.get("detections", [])
        except Exception as e:
            reply = f"Request failed: {e}"
            detections = []

        st.session_state["history"].append(("You", user_input))
        st.session_state["history"].append(("Agent", reply))

        # Show detections with colored panels
        if detections:
            st.subheader("Detected Threats")
            for d in detections:
                attack = d.get("attack", "Unknown")
                ip = d.get("ip", "N/A")
                time = d.get("time", "N/A")

                if attack.lower() == "none":
                    st.success(f"✅ Safe: {time} — No threat detected")
                else:
                    st.error(f"❌ Threat Detected: {attack} at {time} from {ip}")

# Display chat history
st.subheader("Chat History")
for speaker, text in st.session_state["history"]:
    st.markdown(f"**{speaker}:** {text}")