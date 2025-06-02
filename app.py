import gradio as gr
from transformers import pipeline

# Load multilingual model
qa_pipeline = pipeline("question-answering", model="mrm8488/bert-multi-cased-finetuned-xquadv1")

# Chat history
chat_history = []

def read_file(file_obj):
    if file_obj is None:
        return ""

    filename = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
    
    if filename.endswith(".txt"):
        with open(file_obj, "r", encoding="utf-8") as f:
            return f.read()

    elif filename.endswith(".pdf"):
        import PyPDF2
        with open(file_obj, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

    elif filename.endswith(".docx"):
        import docx
        doc = docx.Document(file_obj)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return "Unsupported file type."

def chat(user_question, file, history):
    context = read_file(file)
    if not user_question or not context:
        return history + [[user_question, "Please provide a question and valid file."]]

    try:
        result = qa_pipeline(question=user_question, context=context)
        answer = result["answer"]
    except Exception as e:
        answer = f"Error: {repr(e)}"

    history.append([user_question, answer])
    return history

with gr.Blocks() as demo:
    gr.Markdown("## 🌍 Multilingual Q&A Chatbot with File Upload")
    chatbot = gr.Chatbot(label="Conversation")
    with gr.Row():
        txt = gr.Textbox(label="Ask a question")
        file = gr.File(label="Upload PDF, TXT, or DOCX")
    submit = gr.Button("Submit")
    submit.click(chat, inputs=[txt, file, chatbot], outputs=chatbot)

demo.launch()
