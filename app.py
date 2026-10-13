
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LLM Comparison Benchmark",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LLM Comparison Benchmark")
st.write(
    "Compare sample LLM responses using response length, "
    "simulated latency and a simple structure score."
)

st.info(
    "Demo mode: responses and latency values are illustrative, "
    "not results from live AI models."
)

prompt = st.text_area(
    "Enter a prompt to compare",
    value="Explain Artificial Intelligence in simple words.",
    height=100
)

def create_responses(user_prompt):
    return [
        {
            "Model": "Demo Model A",
            "Response": (
                f"Main idea: {user_prompt}\n\n"
                "Explanation: Focus on the central concept and "
                "explain it in simple, concise language.\n\n"
                "Example: Connect the concept to a familiar "
                "everyday situation."
            ),
            "Latency (seconds)": 0.42
        },
        {
            "Model": "Demo Model B",
            "Response": (
                f"Topic: {user_prompt}\n\n"
                "Key points:\n"
                "- Define the main concept.\n"
                "- Explain how it works.\n"
                "- Mention a practical use.\n\n"
                "Example: Show one real-world application."
            ),
            "Latency (seconds)": 0.68
        },
        {
            "Model": "Demo Model C",
            "Response": (
                f"Question: {user_prompt}\n\n"
                "Simple explanation: Start with a short definition, "
                "then explain the idea step by step.\n\n"
                "Practical example: Describe how the idea could "
                "help solve a common problem.\n\n"
                "Conclusion: Summarize the main takeaway."
            ),
            "Latency (seconds)": 0.53
        }
    ]

def structure_score(response):
    score = 40
    if "Explanation:" in response:
        score += 20
    if "Example:" in response or "example:" in response:
        score += 20
    if "Conclusion:" in response or "Key points:" in response:
        score += 20
    return min(score, 100)

if st.button("Compare Responses", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        results = create_responses(prompt.strip())

        for item in results:
            item["Word Count"] = len(item["Response"].split())
            item["Structure Score"] = structure_score(
                item["Response"]
            )

        df = pd.DataFrame(results)

        st.subheader("Comparison Metrics")

        c1, c2, c3 = st.columns(3)
        c1.metric("Models compared", len(df))
        c2.metric("Average word count", round(df["Word Count"].mean()))
        c3.metric(
            "Average structure score",
            f'{df["Structure Score"].mean():.0f}/100'
        )

        st.subheader("Results Table")
        st.dataframe(
            df[
                [
                    "Model",
                    "Latency (seconds)",
                    "Word Count",
                    "Structure Score"
                ]
            ],
            use_container_width=True
        )

        st.subheader("Response Length")
        st.bar_chart(df.set_index("Model")["Word Count"])

        st.subheader("Simulated Latency")
        st.bar_chart(df.set_index("Model")["Latency (seconds)"])

        st.subheader("Individual Responses")
        for item in results:
            with st.expander(item["Model"]):
                st.write(item["Response"])
                st.caption(
                    f'Words: {item["Word Count"]} | '
                    f'Structure score: {item["Structure Score"]}/100'
                )

        st.download_button(
            "Download Results as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="llm_comparison_results.csv",
            mime="text/csv"
        )

st.caption(
    "Note: Structure score is a rule-based demonstration metric. "
    "It does not measure factual accuracy or overall answer quality."
)
