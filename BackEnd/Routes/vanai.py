from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, current_user
import openai,os, glob, base64, re
from BackEnd.utilities.thread_management import store_thread, check_if_thread_exists
from flask import stream_with_context, Response
from BackEnd.utilities.event_handler import EventHandler
from BackEnd.config import Config
from BackEnd.utilities.image_generator import clean_image_folder


vanai_bp = Blueprint('vanai', __name__)

openai.api_key = Config.OPENAI_API_KEY

@vanai_bp.route('/vanai', methods=['POST'])
@jwt_required()
def vanai():
        email = current_user.email
        print (f'email:,{email}')
        if not email:
            return jsonify({'error': 'User not logged in or email not found in session'}), 401

        client = openai.OpenAI()
        user_question = request.form.get('question') # Get the 'question' field from the JSON data
        if user_question == '':
            user_question = None
        if user_question is not None:
            print('there is question')
        image = request.files.get('imageInput')
 
        if image:
            image_folder = 'BackEnd/static/images'
        # Process image input
            image_path = os.path.join(image_folder, image.filename)
            image.save(image_path)
            print("Received image:", image_path)

         # Clean up old images if there are more than 5
        image_folder = 'BackEnd/static/images'
        clean_image_folder(image_folder) 
        thread_id = check_if_thread_exists(email)
        print(f'thread_id:,{thread_id}')
        if thread_id is None:
            thread = client.beta.threads.create()
            thread_id = thread.id
            store_thread(email, thread_id)
            
            print (f'thread1:,{thread_id}')
        
        try:
                def generate():    
                    
                    event_handler = EventHandler()
                    if image is not None and user_question is None:
                        image_folder = 'BackEnd/static/images'
                        image_path = os.path.join(image_folder, image.filename)
                        file = client.files.create(
                        file=open(image_path, "rb"),
                        purpose="vision"
                        )
                        print('this is step 1')
                        client.beta.threads.messages.create(
                            thread_id=thread_id,
                            role="user",
                           content=[
                    {
                        "type": "text",
                        "text": "what is the image about?"
                    },
                    {
                        "type": "image_file",
                        "image_file": {"file_id": file.id}
                    }
                    ]
                        )
                    elif image is not None and user_question is not None:
                        image_folder = 'BackEnd/static/images'
                        image_path = os.path.join(image_folder, image.filename)
                        file = client.files.create(
                        file=open(image_path, "rb"),
                        purpose="vision"
                        )
                        print('this is step 2')
                        client.beta.threads.messages.create(
                            thread_id=thread_id,
                            role="user",
                           content=[
                    {
                        "type": "text",
                        "text": user_question
                        
                    },
                    {
                        "type": "image_file",
                        "image_file": {"file_id": file.id}
                    }
                    ]
                        )
                    else:
                        print('this is step 3')
                        client.beta.threads.messages.create(
                            thread_id=thread_id,
                            role="user",
                            content=user_question
                        )
                        print(user_question)
                    with client.beta.threads.runs.stream(
                        thread_id=thread_id,
                        assistant_id="asst_PyJRlXavklZFg7WipfSN45Cv",
                        event_handler=event_handler,

                        ) as stream:
                            for event in stream:
                                # Print the text from text delta events
                                if event.event == "thread.message.delta" and event.data.delta.content:
                                    #print(event.data.delta.content[0].text.value, end="", flush=True)
                                    yield (event.data.delta.content[0].text.value)
                    
                    
                    output_text = event_handler.full_text
                    print(f'output_text from vanai : {output_text}')
                    #image_match = re.search(r'!\[.*?\]\((.*?)\)', output_text)
                    #image_match = re.search(r'!\[.*?\]\((.*?)\)|(\bBackEnd/static/images/[^)]+)', output_text)
                    image_match = re.search(r'!\[.*?\]\((.*?)\)|\b(?:[a-f0-9-]{36}\.jpg)\b', output_text)
                    print(f'image_match: {image_match}')
                    if image_match:
                         #image_filename = image_match.group(1).strip()
                         #image_filename = image_match.group(1) or image_match.group(2)
                         image_filename = image_match.group(1) if image_match.group(1) else image_match.group(0).strip()
                         #image_path = os.path.join('BackEnd/static/images', image_filename)
                         image_path = os.path.join('BackEnd/static/images', os.path.basename(image_filename))
                         print(f'image_path from Vanai: {image_path}')
                         if os.path.exists(image_path): 
                            with open(image_path, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            yield f"data:image/jpeg;base64,{encoded_string}\n\n"
                    else:
                        yield f"{output_text}\n\n"
                    # Call suggestions function after the main process
                    #suggestions_response = suggestions()
                    #yield f"{suggestions_response}\n\n"
                             
                return Response(stream_with_context(generate()), mimetype='text/event-stream')                  
        except Exception as e:  
            # Handle any errors that occur during the API call
            answer = f"An error occurred: {str(e)}"
            return jsonify({'answer': answer}),500
        
@vanai_bp.route('/suggestions', methods=['POST'])
@jwt_required()
def suggestions():
     data=request.get_json()
     text_response = data.get('text_response')
     print(f'this is from suggestion: {text_response}')
     if not text_response:
        return jsonify({'error': 'Text response not found '}), 400
     client = openai.OpenAI()
     thread=client.beta.threads.create()
     thread_id=thread.id
     print(f'this is from suggestion thread_id: {thread_id}')
     
     client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="give me 3 concise, short, easy, fun question to ask about this topic :" + text_response)
     full_response = ""
     with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id="asst_QmE7PkXH36ywhUezg9w3hS5u",
        ) as stream:
            for event in stream:
                if event.event == "thread.message.delta" and event.data.delta.content:
                    full_response += event.data.delta.content[0].text.value
     print(full_response)            
              
     next_suggestions_list=[]
     #next_suggestions_regex= re.compile(r'\d+\.\s\*\*(.*?)\*\*')
     next_suggestions_regex = re.compile(r'\d+\.\s+(.*?)(?:\n|$)')
     matches=next_suggestions_regex.findall(full_response)  
     for match in matches:
        next_suggestions_list.append(match.strip())  
     return jsonify(next_suggestions_list)    
          