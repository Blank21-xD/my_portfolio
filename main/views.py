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

        # Mailjet API Keys from Environment Variables
        api_key = os.getenv('MAILJET_API_KEY')
        api_secret = os.getenv('MAILJET_SECRET_KEY')

        # This payload follows Mailjet's v3.1 Send API
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "lama.safal21@gmail.com",
                        "Name": "Portfolio Contact Form"
                    },
                    "To": [
                        {
                            "Email": "lama.safal21@gmail.com",
                            "Name": "Safal"
                        }
                    ],
                    "Subject": f"New Inquiry: {subject}",
                    "TextPart": f"Sender: {user_email}\n\nMessage:\n{message_body}",
                    "HTMLPart": f"<h3>New Message from Portfolio</h3><p><b>From:</b> {user_email}</p><p><b>Message:</b><br>{message_body}</p>"
                }
            ]
        }

        try:
            response = requests.post(
                "https://api.mailjet.com/v3.1/send",
                auth=(api_key, api_secret),
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                messages.success(
                    request, "Your message has been sent successfully!")
            else:
                # Log the error for you, but show a nice message to user
                print(
                    f"Mailjet API Error: {response.status_code} - {response.text}")
                messages.error(
                    request, "Oops! Our mail server is acting up. Please try again later.")

        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            messages.error(
                request, "Connection failed. Please check your internet and try again.")

        return redirect('home')

    return render(request, 'main/home.html', {'projects': projects})
