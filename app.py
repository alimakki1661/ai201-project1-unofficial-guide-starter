"""
app.py — Gradio web UI for The Unofficial Guide
Milestone 5: query interface
"""

import gradio as gr
from query import ask
from retrieval import build_vector_store

# Build vector store once at startup (avoids re-embedding on every query)
print("Starting up The Unofficial Guide...")
collection, model = build_vector_store()
print("Ready.\n")


def handle_query(question: str):
    """Wrapper that takes a question and returns (answer, sources) as strings."""
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question, collection, model)
    answer = result["answer"]
    sources_text = "\n".join(f"• {src}" for src in result["sources"])
    return answer, sources_text


# Build the Gradio interface
with gr.Blocks(title="The Unofficial Guide — CSI CS Professors") as demo:
    gr.Markdown("# The Unofficial Guide")
    gr.Markdown("Ask questions about CSI Computer Science professors based on student reviews.")
    
    question_input = gr.Textbox(
        label="Your question",
        placeholder="e.g. Is attendance mandatory for Professor Jahaj's CSC220 class?",
        lines=2,
    )
    
    ask_button = gr.Button("Ask", variant="primary")
    
    answer_output = gr.Textbox(label="Answer", lines=8)
    sources_output = gr.Textbox(label="Retrieved from", lines=4)
    
    # Wire up both the button click and the Enter key
    ask_button.click(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output],
    )
    question_input.submit(
        handle_query,
        inputs=question_input,
        outputs=[answer_output, sources_output],
    )

if __name__ == "__main__":
    demo.launch()