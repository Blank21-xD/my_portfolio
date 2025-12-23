import os
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project


def home(request):
    projects = Project.objects.all().order_by('-created_at')

    if request.method == "POST":
        user_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message')

        # Get keys from Render environment
        api_key = os.getenv('MAILJET_API_KEY')
        api_secret = os.getenv('MAILJET_SECRET_KEY')

        # Mailjet API Payload
        data = {
            'Messages': [
                {
                    "From": {"Email": "lama.safal21@gmail.com", "Name": "Portfolio Site"},
                    "To": [{"Email": "lama.safal21@gmail.com", "Name": "Safal"}],
                    "Subject": f"New Message: {subject}",
                    "TextPart": f"Sender: {user_email}\n\nMessage: {message_body}",
                }
            ]
        }

        # Send via HTTPS (Port 443) - This cannot be blocked!
        response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(api_key, api_secret),
            json=data
        )

        if response.status_code == 200:
            messages.success(request, "Success! Your message has been sent.")
        else:
            # Shows error if API keys are wrong
            messages.error(request, f"Error: {response.status_code}")
            print(f"Mailjet Error: {response.text}")

        return redirect('home')

    return render(request, 'main/home.html', {'projects': projects})
