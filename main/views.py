from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import Project


def home(request):
    # 1. Fetch projects for the 'GET' request (showing the page)
    # This ensures projects are available even if the form fails
    projects = Project.objects.all().order_by('-created_at')

    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            send_mail(
                f"Portfolio Message: {subject}",
                f"From: {email}\n\n{message}",
                'lama.safal21@gmail.com',  # From
                ['lama.safal21@gmail.com'],  # To
                fail_silently=False,
            )
            messages.success(request, "Thank you! Your message has been sent.")
        except Exception as e:
            messages.error(
                request, "Oops! Something went wrong sending your message.")

        # Always redirect after a POST to prevent double-submits
        return redirect('home')

    # 2. Package data into context for the template
    context = {
        'projects': projects
    }

    return render(request, 'main/home.html', context)
