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

@vanai_bp.route('/vanai', methods=['GET','POST'])
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
                                    print(event.data.delta.content[0].text.value, end="", flush=True)
                                    yield (event.data.delta.content[0].text.value)
                    output_text = event_handler.full_text
                    print(f"Output text: {output_text}")

                    image_match = re.search(r'!\[.*?\]\((.*?)\)', output_text)
                    if image_match:
                         image_filename = image_match.group(1).strip()
                         image_path = os.path.join('BackEnd/static/images', image_filename)
                         if os.path.exists(image_path): 
                            with open(image_path, "rb") as image_file:
                                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            yield f"data:image/jpeg;base64,{encoded_string}\n\n"
                    else:
                        yield f"{output_text}\n\n"
                             
                return Response(stream_with_context(generate()), mimetype='text/event-stream')                  
        except Exception as e:  
            # Handle any errors that occur during the API call
            answer = f"An error occurred: {str(e)}"
            return jsonify({'answer': answer}),500