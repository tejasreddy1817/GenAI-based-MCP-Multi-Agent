import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart Research Assistant (MCP)", layout="wide")

st.title("🤖 Smart Research Assistant (MCP-Based Architecture)")
st.write("This version fetches live content, generates an image, and allows document download.")

# Sidebar
with st.sidebar:
    st.header("Options")
    use_web = st.checkbox("Use live SerpAPI search", value=False)
    use_openai = st.checkbox("Use OpenAI for summarization", value=False)
    show_raw = st.checkbox("Show intermediate data", value=True)
    max_docs = st.number_input("Max docs to fetch", min_value=1, max_value=10, value=3)
    run_btn = st.button("Run Workflow")

topic = st.text_input("Enter your research topic", "")

if run_btn and topic.strip():
    st.header(f"Results for: {topic}")

    # Step 1: Search
    st.subheader("🔍 Step 1: Searching Documents")
    search_res = requests.post(f"{MCP_SERVER_URL}/search_tool", json={
        "query": topic, "max_results": int(max_docs), "use_web": use_web
    }).json()
    docs = search_res.get("documents", [])
    for i, d in enumerate(docs):
        st.markdown(f"**Doc {i+1}: {d['title']}**")
        st.write(d['content'])
        st.divider()

    # Step 2: Analysis
    st.subheader("🧠 Step 2: Analyzing Data")
    analysis = requests.post(f"{MCP_SERVER_URL}/analyze_tool", json={"docs": docs}).json()["analysis"]
    if show_raw: st.json(analysis)

    # Step 3: Summarization
    st.subheader("📝 Step 3: Generating Summary")
    summary = requests.post(f"{MCP_SERVER_URL}/summarize_tool", json={
        "topic": topic, "docs": docs, "analysis": analysis
    }).json()["summary"]
    st.markdown(summary)

    # 🖼️ Step 4: Generating Image
    st.subheader("🖼️ Step 4: Generating Image")
    try:
        resp = requests.post(f"{MCP_SERVER_URL}/image_tool",
                            json={"topic": topic, "docs": docs, "analysis": analysis})
        if resp.status_code != 200:
            st.error(f"❌ Server returned {resp.status_code}")
        else:
            try:
                data = resp.json()
            except Exception:
                st.error("⚠️ Server did not return JSON.")
                st.text(resp.text[:200])  # show first chars of response for debugging
            else:
                if data.get("image_url"):
                    st.image(data["image_url"], caption=f"AI-generated image for '{topic}'",
                            use_column_width=True)
                elif data.get("error"):
                    st.warning(f"⚠️ Image generation failed: {data['error']}")
                else:
                    st.warning("⚠️ No image URL in response.")
    except Exception as e:
        st.error(f"Image generation failed: {e}")


    # Step 5: Validation
    st.subheader("✅ Step 5: Validation Report")
    val_report = requests.post(f"{MCP_SERVER_URL}/validate_tool", json={
        "summary": summary, "docs": docs, "analysis": analysis
    }).json()["validation"]
    st.json(val_report)

    # Step 6: Formatting & Download
    st.subheader("📄 Step 6: Formatting & Downloading Output")
    md = requests.post(f"{MCP_SERVER_URL}/format_tool", json={
        "topic": topic, "summary": summary, "analysis": analysis
    }).json()["markdown"]
    st.download_button("⬇️ Download Markdown Document", md, file_name=f"{topic}.md")
    st.markdown(md)
else:
    st.info("Enter a topic and click **Run Workflow**.")
