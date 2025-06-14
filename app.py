import streamlit as st
import pandas as pd
from enrich import enrich_lead
from fake_detect import detect_fake_website
from search_filter import smart_search

st.set_page_config(page_title="SmartLead - Lead Quality Intelligence", layout="wide")
st.title("🚀 SmartLead - Lead Quality Intelligence")

st.sidebar.header("🔍 Lead Search")
domain = st.sidebar.text_input("Search Keyword (e.g., AI, fintech, edtech)")
location = st.sidebar.text_input("Location (e.g., USA, India)")

if st.sidebar.button("🔎 Search Companies"):
    if domain.strip() == "":
        st.sidebar.warning("Please enter a valid search keyword.")
    else:
        with st.spinner("Searching for companies..."):
            try:
                results = smart_search(domain, location)
                st.session_state["search_results"] = results
                st.success("✅ Companies fetched successfully!")
            except Exception as e:
                st.error(f"❌ Error occurred: {e}")

if "search_results" in st.session_state:
    st.subheader("🔎 Search Results")

    df = pd.DataFrame(st.session_state["search_results"])
    
    if df.empty or "company" not in df.columns:
        st.warning("⚠️ No company data available.")
    else:
        st.write("Top company leads based on your query:")
        available_cols = [col for col in ["company", "domain", "location", "description"] if col in df.columns]
        st.dataframe(df[available_cols], use_container_width=True)

        selected = st.multiselect("Select companies to enrich", df["company"].dropna().unique().tolist())
        selected_df = df[df["company"].isin(selected)]

        if not selected_df.empty and st.button("🧠 Enrich & Score"):
            st.subheader("📊 Enriched Results")
            enriched_data = []

            with st.spinner("Enriching selected companies and detecting fake websites..."):
                for _, row in selected_df.iterrows():
                    try:
                        enriched = enrich_lead(row.get("domain", ""))
                        fake_status = detect_fake_website(row.get("domain", ""))

                        if isinstance(fake_status, dict):
                            enriched.update(fake_status)

                        enriched["company"] = row.get("company", "N/A")
                        enriched["domain"] = row.get("domain", "N/A")
                        
                    except Exception as e:
                        enriched = {
                            "company": row.get("company", "N/A"),
                            "domain": row.get("domain", "N/A"),
                            "error": str(e)
                        }
                    enriched_data.append(enriched)

            enriched_df = pd.DataFrame(enriched_data)
            st.dataframe(enriched_df, use_container_width=True)
