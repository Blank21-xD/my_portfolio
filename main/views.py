from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Project


def home(request):
    projects = Project.objects.all().order_by('-created_at')

    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"New Feedback from: {email}\n\nSubject: {subject}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=f"Portfolio Inquiry: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(
                request, "Thank you! Your message has been sent successfully.")
        except Exception as e:
            # CHANGE: This will now show the REAL error on your website screen
            error_msg = str(e)
            print(f"Email Error: {error_msg}")
            messages.error(request, f"Email Error Details: {error_msg}")

        return redirect('home')

    context = {'projects': projects}
    return render(request, 'main/home.html', context)
