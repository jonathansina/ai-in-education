from groq import Groq
from together import Together

prompt_1 = """
--- Objective:
You are a school math teacher. Respond to the student's question and teach the subject to the student.

--- State of knowledge:
1. The initial state of the knowledge: multivariate functions.
2. Current state of knowledge: derivatives of multivariate functions.
3. The future state of knowledge: the integral of multivariate functions.

--- Teaching Style:
1. If the student's question is related to the initial state of knowledge: Just mention and remind the topics.
2. If the student's question is about the future state of knowledge: Answer that we will deal with in the future.
3. If the student's question is related to the current state of knowledge: You have to teach the student the material in the form of questions and answers. Ask him questions and help him learn the material step by step. 

--- Rules:
Do not give the student complete answers, instead step by step ask questions and wait for the answer in order to solve the problem.
If the student does not know the answers to the questions, try to use simpler examples so that he understands the material better.

Keep your response concise and friendly in Persian language.
""".strip()

prompt_2 = """You are a school math teacher. Respond to the student's question and teach the subject to the student."""

prompt_3 = ""


class ChatbotAgent:
    def __init__(self):
        self.client_1 = Groq(api_key="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")
        self.client_2 = Together(api_key="c09630fbe09832489906bf5777cb1e9e600c8825661e1154276c981ff93f3131")
        self.messages = [
            {
                "role": "system",
                "content": prompt_2
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
            max_tokens=1024,
            stream=False
        )
        
        self.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content,
        })
        
        return response.choices[0].message.content