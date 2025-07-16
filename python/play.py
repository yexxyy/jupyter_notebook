#!/usr/bin/env python
# -*- coding: utf-8 -*-
# play.py in jupyter_notebook
# Created by yetongxue at 2024/11/3
import os

from manim import *
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
DEEPSEEK_APIKEY = os.environ.get('DEEPSEEK_APIKEY')


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


def main():
    client = OpenAI(api_key=DEEPSEEK_APIKEY, base_url="https://api.deepseek.com")

    messages = []
    while True:
        msg = input('提问: ')
        messages.append({"role": "user", "content": msg})
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        messages.append({"role": "system", "content": response.choices[0].message.content})
        print(f'回复: {response.choices[0].message.content}')


if __name__ == '__main__':
    main()
