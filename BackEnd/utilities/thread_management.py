from BackEnd.model import db, Thread, ThreadID
import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')
def store_thread(email, thread_id):
    if thread_id is None:
            thread_id = generate_new_thread_id()
            thread = Thread(email=email, thread_id=thread_id)
            db.session.add(thread)
            db.session.commit()
    try:
        
        thread = Thread.query.filter_by(email=email).first()
        if not thread:
            thread = Thread(email=email, thread_id=thread_id)
            db.session.add(thread)
            db.session.commit()
        new_thread_id = ThreadID(thread_id=thread_id, thread_ref_id=thread.id)
        db.session.add(new_thread_id)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error storing thread: {e}")

def check_if_thread_exists(email):
    thread = Thread.query.filter_by(email=email).first()
    if thread and thread.thread_ids:
        return thread.thread_ids[-1].thread_id  # Return the latest thread_id
    return None

def generate_new_thread_id():
    client = openai.OpenAI()   
    thread = client.beta.threads.create()
    return thread.id