API_KEY = "AIzaSyBB-Hx05N7Xqf4IQYuy7yMRzjowxKmz7_o"

from google import genai

# client = genai.Client(api_key=API_KEY)
# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Explain how AI works"
# )
# print(response.text)

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=["Tell me about you, 50 words"])
for chunk in response:
    print(chunk.text, end="")