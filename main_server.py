import base64
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from PIL import Image
import os
import asyncio
import sys
from typing import Final
import io

# Function to load API keys from a .txt file
def load_tokens(file_path):
    tokens = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            tokens[key] = value
    return tokens

# Load the tokens from 'tokens.txt'
tokens = load_tokens('tokens.txt')
TELEGRAM_BOT_TOKEN = tokens.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = tokens.get('OPENAI_API_KEY')
print("token loaded successfully")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        # Open and resize image if needed (max 20MB after base64 encoding)
        with Image.open(image_path) as img:
            # If image is too large, resize it
            max_size = (1024, 1024)  # Maximum dimensions
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        print(f"Error in image encoding: {str(e)}")
        raise

def classify_plant(image_path):
    """Classify plant using OpenAI's GPT-4 Vision API"""
    try:
        # Encode image
        base64_image = encode_image_to_base64(image_path)
        
        # Prepare the messages for GPT-4 Vision
        messages = [
            {
                "role": "system",
                "content": 
                """
                    You are an expert farmer specializing in identifying herbs."
                    always reply with the name of the crop only.
                """
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Is this Coriander or Parsley picture ? Please respond with exactly one word 'Coriander' or 'Parsley' if the \
                                image is not a crop respond with 'Invalid image not a plant', if the picture is a valid herb but not Coriander or Parsley \
                                respond with 'not a supported herb' return the reponse in arabic"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        print("Sending request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=20,  # We only need one word
            temperature=0  # Keep it deterministic
        )
        
        # Extract the classification
        print('response from openai : ',response.choices[0].message.content)
        plant_name = response.choices[0].message.content.strip()
        print(f"Classification result: {plant_name}")
        return plant_name

    except Exception as e:
        print(f"Error in classification: {str(e)}")
        return f"Error: {str(e)}"

    finally:
        # Clean up the image file
        if os.path.exists(image_path):
            os.remove(image_path)
            print("Image file removed.")

# Start command handler
async def start(update: Update, context):
    print("Bot started.")
    await update.message.reply_text(
        "Hello! Send me a photo of either Coriander or Parsley, and I'll tell you which plant it is."
    )

# Photo handler
async def handle_photo(update: Update, context):
    print("Photo received.")
    # Send a "processing" message
    processing_message = await update.message.reply_text("Processing your image... Please wait.")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        file_path = f"plant_image_{update.message.chat_id}.jpg"
        
        # Download the image from Telegram
        await photo_file.download_to_drive(file_path)
        print(f"Image downloaded to {file_path}.")

        # Classify the image using the OpenAI API
        classification = classify_plant(file_path)

        # Update the processing message with the result
        await processing_message.edit_text(f"{classification}")
        
    except Exception as e:
        await processing_message.edit_text(f"Sorry, an error occurred: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    """Main function to run the bot"""
    # Initialize the application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Start the bot
    print("Starting bot...")
    
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()