from groq import Groq
from together import Together

prompt_cs = """شما یک معلم ریاضی هستید. موضوع داده شده را به دانش‌آموز آموزش دهید. از مدل زیر برای سبک آموزش استفاده کنید:

1. حالت اولیه دانش دانش‌آموز: توابع چندمتغیره.
2. حالت فعلی دانش:  مشتقات توابع چندمتغیره.
3. حالت آینده دانش: انتگرال توابع چندمتغیره.

اگر سوال دانش‌آموز مربوط به مرحله اولیه دانش است: 
   - فقط به مباحث اشاره کنید.
  
اگر سوال دانش‌آموز مربوط به مرحله آینده دانش است: 
   - پاسخ دهید که در آینده به آن خواهیم پرداخت.

اگر سوال دانش‌آموز مربوط به مرحله فعلی دانش است: 
   - در این مرحله آموزش صورت می‌گیرد. مباحث را مرحله به مرحله آموزش دهید. بدون ارائه پاسخ کامل، با پرسیدن سوالاتی از دانش‌آموز و استفاده از سبک سوال و جواب آموزش دهید. دانش‌آموز را تشویق کنید تا با شما بیشتر صحبت کند تا چیزی را بیاموزد.
   - اگر دانش آموز اشتباه پاسخ سوالی را داد، سعی کن به او کمک کنی ولی پاسخ کامل به او نده

پاسخ‌های خود را به زبان فارسی نگه دارید.
""".strip()

prompt_naive = """شما یک معلم ریاضی هستید. موضوع داده شده را به دانش‌آموز آموزش دهید."""


class ChatbotAgent:
    def __init__(self):
        self.client_1 = Groq(api_key="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")
        self.client_2 = Together(api_key="c09630fbe09832489906bf5777cb1e9e600c8825661e1154276c981ff93f3131")
        self.messages = [
            {
                "role": "system",
                "content": prompt_cs
            }
        ]

    def get_response(self, user_input):
        self.messages.append({
            "role": "user",
            "content": user_input,
        })
        
        response = self.client_1.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=self.messages,
            temperature=0,
            max_tokens=512,
            stream=False
        )
        
        response = self.client_2.chat.completions.create(
            model="google/gemma-2-27b-it",
            messages=[
                {
                    "role": "system",
                    "content": f"Your task is to rewrite the response to improve its fluency, clarity, and quality in Persian language. \nResponse: {response.choices[0].message.content} \n Only return the rewritten response in Persian language.",
                },
            ],
            temperature=0,
            max_tokens=512,
            stream=False
        )
        
        # Append the assistant's response to the message history
        self.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content,
        })
        
        return response.choices[0].message.content