from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project


def home(request):
    # Fetch projects for the display
    projects = Project.objects.all().order_by('-created_at')

    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Combine info for the email body
        full_message = f"New Feedback from: {email}\n\nSubject: {subject}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=f"Portfolio Inquiry: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Set in settings.py
                # Sends TO your gmail
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(
                request, "Thank you! Your message has been sent successfully.")
        except Exception as e:
            # This helps you see the error in Render logs if it fails
            print(f"Email Error: {e}")
            messages.error(
                request, "Oops! Something went wrong. Please try again later.")

        # Always redirect after POST to clear the form and prevent double-sending
        return redirect('home')

    context = {
        'projects': projects
    }
    return render(request, 'main/home.html', context)
