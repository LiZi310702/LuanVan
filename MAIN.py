import tkinter as tk
from tkinter import *
import google.generativeai as genai
from IPython.display import Markdown
import requests
from PIL import Image, ImageTk
from requests.exceptions import ChunkedEncodingError
from io import BytesIO


genai.configure(api_key="AIzaSyAsFKdWZzmSTXnSD5yrPRNuhYX-a3zGM00")
model = genai.GenerativeModel('gemini-pro')

openai_api_key = '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'

def TomTat():
    print("Start call Api...")
    input_text = T1.get("1.0", END)
    response = model.generate_content("Vui lòng từ đoạn văn bản trên, hãy tạo các promt cho mô hình sinh ảnh,chỉ giữ lại các thông tin có giá trị,loại bỏ các văn bản liên quan đến cách dùng từ hoa mỹ văn học, cách nhau bởi dấu phẩy, chuyển nó sang tiếng anh"+input_text)
    data = response.candidates[0].content.parts[0].text
    T.insert(tk.END, data)
    print("Call success...")

def CreatePromt():
    print("Start call Api...")
    input_text = T1.get("1.0", END)
    response = model.generate_content("Mô tả khung cảnh trên, sau đó tóm tắt nó để tạo thành promt cần có cho mô hình sinh ảnh, chỉ giữ lại các từ mô tả cảnh vật, cách nhau bởi dấu phẩy, chuyển nó sang tiếng anh, không cần hiển thị văn bản gốc, chỉ cần hiển thị promt bằng tiếng anh"+input_text)
    data = response.candidates[0].content.parts[0].text
    T.insert(tk.END, data)
    print("Call success...")

url = 'https://api.openai.com/v1/images/generations'
# Request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_api_key}'
}

def download_image_with_retry(url, max_retries=3):
    for _ in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.content
        except ChunkedEncodingError as e:
            print(f"Error: {e}. Retrying...")
    print(f"Failed to download image after {max_retries} retries.")
    return None

def display_image(img_url):
    image_data = download_image_with_retry(img_url)
    if image_data:
        img = Image.open(BytesIO(image_data))

        # Create a new window to display the image
        image_window = tk.Toplevel(root)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(image_window, image=photo)
        label.image = photo
        label.pack()
    else:
        print("Image download failed.")

def GenerateImage():
    print("Start generating image...")
    input_text = T.get("1.0", "end-1c")
    prompt_text = " ".join(input_text.split())
    response = requests.post(url, headers=headers, json={"model": "dall-e-2", "prompt": prompt_text, "n": 1, "size": "512x512"})
    result = response.json()
    #print(result)
    # Extract URL from the response
    image_url = result["data"][0]["url"] if "data" in result and result["data"] and "url" in result["data"][0] else None
    #print(image_url)
    display_image(image_url)


root = Tk()
root.geometry("550x500")


   
# Create text widgets and specify size.
T = Text(root, height=15, width=52)
T1 = Text(root, height=5, width=52)

def clearText():
   T.delete('1.0', END)
   T1.delete('1.0',END)

# Create labels
Input = Label(root, text="INPUT")
Output = Label(root, text="OUTPUT")

# Place labels using grid
Input.grid(row=1, column=0, padx=10, pady=5, sticky="w")
Output.grid(row=2, column=0, padx=10, pady=5, sticky="w")

# Create button for API call
b1 = Button(root, text="TÓM TẮT", command=TomTat)
b2 = Button(root, text="SINH PROMT", command=CreatePromt)
# Create buttons for clearing and exiting
b3 = Button(root, text="CLEAR", command=clearText)
b4 = Button(root, text="EXIT", command=root.destroy)

# Create button for image generation
b5 = Button(root, text="SINH ẢNH", command=GenerateImage)

# Use grid to place widgets
T1.grid(row=1, column=1, padx=10, pady=5, columnspan=2)
T.grid(row=2, column=1, padx=10, pady=5, columnspan=2)
b1.grid(row=3, column=0, columnspan=3, pady=5)

b2.grid(row=3, column=2, columnspan=3, pady=5)

b3.grid(row=4, column=0, columnspan=3, pady=5)
b4.grid(row=4, column=2, columnspan=3, pady=5)
b5.grid(row=5, column=1, pady=5, columnspan=2)
root.mainloop()