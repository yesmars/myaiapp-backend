import openai
import os,glob,base64,uuid

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


client = openai.OpenAI()

def generate_image(description):
    # Generate the image with DALL-E
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1
    )
    
    image_data=image_response.data[0].b64_json
    image_bytes = base64.b64decode(image_data)
    directory = 'BackEnd/static/images/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Code to delete oldest images if there are more than 10
    image_files = glob.glob(os.path.join(directory, '*.jpg'))
    image_files.sort(key=os.path.getmtime)
    while len(image_files) > 3:
        os.remove(image_files[0])
        del image_files[0]
    
    # Save the image to a file in the specified directory
    image_filename = f'output_image_{uuid.uuid4()}.jpg'
    image_path = os.path.join(directory, image_filename)
    print(image_path)
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
    return image_filename

def clean_image_folder(folder_path, max_images=5):
    """Remove the oldest images if there are more than `max_images` in the folder."""
    images = glob.glob(os.path.join(folder_path, '*'))
    if len(images) > max_images:
        images.sort(key=os.path.getmtime)  # Sort by modification time
        images_to_remove = images[:-max_images]  # Keep only the latest `max_images` images
        for image in images_to_remove:
            os.remove(image)
            print(f'Removed old image: {image}')