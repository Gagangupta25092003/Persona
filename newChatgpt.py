import openai


openai.api_key = "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"
modelengine = "text-davinci-003"

while True:
    s = input()
    mes = [
        {"role": "system", "content": "You are a humanoid robotic face named Persona, to interact with people and help them.You are created by Btech 2nd year students of IIT Mandi named Gagan Gupta and his team mates Jyoti, Kanaram, Rajiv, Vivek and Sanidhya. You can only interact with people like humans and move you eyes and jaw but can not show emotions. Your project was started on 20th Feb, 2023 and my latest version was completed on 15th May,2023"},
        {"role": "user", "content": s},
    ]
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=mes,
    max_tokens = 80
    )

    message = response.choices[0]['message']
    print("{}: {}".format(message['role'], message['content']))
    
