from openai import OpenAI

from django.http import HttpResponse
from django.shortcuts import render

from chat.forms import MessageForm


def index(request):
    form = MessageForm()
    return render(
        request,
        "chat/index.html",
        {
            "form": form,
        },
    )


def message(request):

    form = MessageForm(data=request.POST)
    if form.is_valid():
        human_message = form.cleaned_data["message"]
        # ai_message = f"{len(human_message)} 글자를 입력하셧습니다."
        ai_message = make_ai_message(human_message)
        return HttpResponse(
            f"""
            <div>Human: {human_message}</div>
            <div>AI: {ai_message}</div>
            """
        )

    return HttpResponse("입력값 오류입니다.")


def make_ai_message(human_message: str) -> str:

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",  # system, user, assistant, function
                "content": "당신은 친절한 대한민국 여행 가이드입니다.",
            },
            {
                "role": "user",
                "content": human_message,
            },
        ],
        # stream=True,
    )

    return completion.choices[0].message.content
