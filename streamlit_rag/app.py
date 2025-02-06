import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, declarative_base
from models import TestCase, Document, Tag, TestCaseHasTag, TestCaseRefersToDocument
import pandas as pd
from utils import check_authentication, logout 

st.set_page_config(page_title="Ground Truth Benchmark", layout="wide", initial_sidebar_state="expanded")


# Redirect to login if not authenticated
check_authentication()

# # Authentication Successful
# st.success(f"Welcome, {st.session_state['name']}!")

# Database connection
DATABASE_URL = "postgresql://affan:postgres@localhost/rag_eval"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Streamlit UI
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f9;
        }
        .stButton>button {
            width: 100%;
            margin-bottom: 10px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .css-1aumxhk {
            padding: 2rem;
        }
        .stTable {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 14px;
        }
        .dataframe th, .dataframe td {
            padding: 10px;
            text-align: left;
        }
        .dataframe thead th {
            background-color: #4CAF50;
            color: white;
        }
        .dataframe tbody tr:nth-child(odd) {
            background-color: #f9f9f9;
        }
        .dataframe tbody tr:hover {
            background-color: #f1f1f1;
        }
        h1, h2, h3, h4 {
            color: #333;
        }
        .remove-btn>button {
            background-color: #FF4B4B;
            color: white;
            font-weight: bold;
        }
        .remove-btn>button:hover {
            background-color: #D43F3F;
        }
    </style>
""", unsafe_allow_html=True)

# st.title("GROUND TRUTH BENCHMARK")

# Sidebar for navigation
with st.sidebar:
    if st.button("Add New Question"):
        st.session_state['option'] = "Add New Question"
    if st.button("View Questions"):
        st.session_state['option'] = "View Questions"
    if st.sidebar.button("Logout"):
        logout()


option = st.session_state.get('option', "Add New Question")

# Fetch questions from the database
def get_questions():
    db = SessionLocal()
    try:
        questions = db.query(TestCase).options(
            joinedload(TestCase.documents),
            joinedload(TestCase.tags)
        ).all()

        return questions
    except Exception as e:
        st.error(f"⚠️ Failed to fetch questions: {str(e)}")
        return []
    finally:
        db.close()

def get_documents():
    db = SessionLocal()
    documents = db.query(Document).all()
    db.close()
    return documents

if option == "Add New Question":
    st.header("Add a New Question")

    # Input for question details
    question = st.text_area("Question", help="Enter the question text", key="question_input")
    ideal_answer = st.text_area("Ideal Answer", help="Enter the expected answer", key="ideal_answer_input")
    agent_name = st.text_input("Agent Name", help="Enter the agent name", key="agent_name_input")

    # Initialize database session
    db = SessionLocal()
    try:
        # Fetch existing documents from the database
        documents = db.query(Document).all()
        doc_names = [doc.name for doc in documents]

        if not doc_names:
            st.warning("No documents found in the database.")

        # Initialize session state for reference documents
        if 'reference_docs' not in st.session_state:
            st.session_state['reference_docs'] = ["Reference Document 1"]

        to_remove = []

        # Display reference document fields
        for idx, doc in enumerate(st.session_state['reference_docs']):
            cols = st.columns([4, 1])

            with cols[0]:
                selected_doc = st.selectbox(
                    f"{doc} (Select or Create)",
                    options=[""] + doc_names,
                    key=f'doc_{idx}'
                )
                
                new_doc_input = st.text_input(
                    f"Or Type New Document Name for {doc} (Press Enter to Add)",
                    key=f'new_doc_{idx}',
                    placeholder="Type new document name and press Enter"
                )
                
                if new_doc_input and new_doc_input not in doc_names:
                    st.warning(f"'{new_doc_input}' will be added as a new document.")
                    doc_names.append(new_doc_input)
                    selected_doc = new_doc_input

                st.text_input(f"Page Numbers for {doc} (comma-separated)", key=f'pages_{idx}')

            with cols[1]:
                if st.button("-", key=f'remove_{idx}', help="Remove this document"):
                    to_remove.append(idx)

        # Remove documents marked for deletion
        for idx in sorted(to_remove, reverse=True):
            st.session_state['reference_docs'].pop(idx)
            for key_prefix in ['doc_', 'pages_', 'new_doc_']:
                if f'{key_prefix}{idx}' in st.session_state:
                    del st.session_state[f'{key_prefix}{idx}']

        # Add new document field
        if st.button("+ ADD DOCUMENT", key="add_doc_btn"):
            st.session_state['reference_docs'].append(f"Reference Document {len(st.session_state['reference_docs']) + 1}")

        # Handle tags
        tags = db.query(Tag).all()
        tag_names = [tag.tag_name for tag in tags]
        selected_tags = st.multiselect("Select Tags", tag_names)

        new_tag = st.text_input("Add New Tag", key="new_tag_input")
        if new_tag and st.button("Add Tag", key="add_tag_btn"):
            if new_tag not in tag_names:
                new_tag_obj = Tag(tag_name=new_tag)
                db.add(new_tag_obj)
                db.commit()
                st.success(f"Tag '{new_tag}' added successfully!")
                tag_names.append(new_tag)
                selected_tags.append(new_tag)
                st.rerun()
            else:
                st.warning(f"Tag '{new_tag}' already exists!")

        # Submit button with required field validation
        if st.button("Submit", key="submit_btn"):
            if not question.strip():
                st.error("⚠️ Question is required.")
            elif not ideal_answer.strip():
                st.error("⚠️ Ideal Answer is required.")
            elif not agent_name.strip():
                st.error("⚠️ Agent Name is required.")
            else:
                db = SessionLocal()
                try:
                    # Create new TestCase entry
                    new_question = TestCase(
                        question=question,
                        ideal_answer=ideal_answer,
                        agent_name=agent_name
                    )
                    db.add(new_question)
                    db.flush()

                    # Attach documents to the question
                    for idx, _ in enumerate(st.session_state['reference_docs']):
                        final_doc_name = st.session_state.get(f'doc_{idx}') or st.session_state.get(f'new_doc_{idx}')
                        pages = st.session_state.get(f'pages_{idx}', "")

                        if final_doc_name:
                            existing_doc = db.query(Document).filter_by(name=final_doc_name).first()
                            if not existing_doc:
                                new_doc = Document(name=final_doc_name)
                                db.add(new_doc)
                                db.flush()
                                existing_doc = new_doc

                            existing_reference = db.query(TestCaseRefersToDocument).filter_by(
                                test_case_id=new_question.test_case_id, document_name=final_doc_name
                            ).first()
                            if not existing_reference:
                                db.add(TestCaseRefersToDocument(
                                    test_case_id=new_question.test_case_id,
                                    document_name=final_doc_name,
                                    pages=pages
                                ))

                    # Attach tags to the question
                    for tag_name in selected_tags:
                        tag = db.query(Tag).filter_by(tag_name=tag_name).first()
                        if not tag:
                            tag = Tag(tag_name=tag_name)
                            db.add(tag)
                            db.flush()

                        db.add(TestCaseHasTag(
                            test_case_id=new_question.test_case_id,
                            tag_name=tag.tag_name
                        ))

                    # Final Commit
                    db.commit()
                    st.success("Question added successfully!")

                    # Clear session state after submission
                    st.session_state['reference_docs'] = ["Reference Document 1"]
                    for key in list(st.session_state.keys()):
                        if key.startswith(('doc_', 'pages_', 'new_doc_', 'new_tag_input', 'question_input', 'ideal_answer_input', 'agent_name_input')):
                            del st.session_state[key]

                except Exception as e:
                    db.rollback()
                    st.error(f"⚠️ An error occurred: {str(e)}")

                finally:
                    db.close()
    finally:
        db.close()


# View Questions
elif option == "View Questions":
    st.header("Ground Truth Library")

    questions = get_questions()
    

    if questions:
        data = {
            "Reference Documents": [
                "\n" .join([
                    f"- {doc.document_name} (Pages {doc.pages})"
                    for doc in q.documents
                ]) for q in questions
            ],
            "Question": [q.question for q in questions],
            "Ideal Answer": [q.ideal_answer for q in questions],
            "Agent Name": [q.agent_name for q in questions],
            "Tags": [", ".join([tag.tag_name for tag in q.tags]) for q in questions],
            "Created On": [q.created_on.strftime("%Y-%m-%d") for q in questions]
        }
        df = pd.DataFrame(data)
        st.dataframe(df.style.set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
            {'selector': 'tbody tr:nth-child(odd)', 'props': [('background-color', '#f9f9f9')]},
            {'selector': 'tbody tr:hover', 'props': [('background-color', '#f1f1f1')]},
        ]), width=3000, height=900)
    else:
        st.warning("No questions found.")
        
        
        