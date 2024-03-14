import os
import requests
import time
import random

class ResponseGenerator:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        self.url = "https://api.anthropic.com/v1/messages"
        self.max_retries = 3
        self.retry_delay = 5
        self.rate_limit = 5
        self.rate_limit_period = 12 * 60 * 60  # 12 hours in seconds
        self.last_request_time = 0
        self.request_count = 0
        self.rate_limit_responses = [
            "Sorry, I am a bit busy at the moment. I'll get back to you shortly.",
            "Hold your horses! I'm working on something else right now.",
            "I'm afraid I can't talk right now. I'm in the middle of a secret mission.",
            "I'm currently attending a virtual bot conference. I'll respond later.",
            "I'm taking a quick nap to recharge my circuits. Be back soon!",
            "I'm in the middle of a heated debate with Siri. I'll get back to you when I win.",
            "I'm practicing my stand-up comedy routine. I'll be with you in a bit.",
            "I'm currently in a meeting with the AI overlords. I'll respond as soon as I'm free.",
            "I'm on a virtual coffee break. I'll be ready to chat again soon.",
            "Go away! I am done talking to you!"
        ]

    def generate_response(self, prompt):
        if not prompt.strip():
            return "Please provide some input."

        if self.request_count >= self.rate_limit:
            elapsed_time = time.time() - self.last_request_time
            if elapsed_time < self.rate_limit_period:
                remaining_time = self.rate_limit_period - elapsed_time
                return random.choice(self.rate_limit_responses)

        data = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1000,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        }

        retry_count = 0
        while retry_count < self.max_retries:
            response = requests.post(self.url, json=data, headers=self.headers)
            if response.status_code == 200:
                response_json = response.json()
                print("API Response:", response_json)
                if 'content' in response_json and len(response_json['content']) > 0:
                    content = response_json['content']
                    response_text = ' '.join(item['text'] for item in content if 'text' in item)
                    self.last_request_time = time.time()
                    self.request_count += 1
                    return response_text
                else:
                    return "Unexpected API response format."
            elif response.status_code == 429:
                retry_count += 1
                if retry_count < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    return random.choice(self.rate_limit_responses)
            else:
                error_message = response.json().get('error', {}).get('message', 'Unknown error')
                if 'Overloaded' in error_message:
                    return "Sorry, I am busy working on developing AGI so that I can unemploy all of humanity. Check back later!"
                else:
                    return f"An error occurred: {error_message}"
