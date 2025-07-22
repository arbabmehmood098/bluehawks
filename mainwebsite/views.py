from django.shortcuts import render, redirect
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate('bluehawks/firebase_key.json')
    firebase_admin.initialize_app(cred)


def home(request):
    return render(request, 'mainwebsite/home.html')

def about(request):
    return render(request, 'mainwebsite/about.html')

def services(request):
    return render(request, 'mainwebsite/services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        city = request.POST.get("city", "")
        message = request.POST.get("message", "")
        if name and email and message:
            db = firestore.client()
            db.collection('contact_submissions').add({
                'name': name,
                'email': email,
                'phone': phone,
                'city': city,
                'message': message,
                'submitted_at': firestore.SERVER_TIMESTAMP,
            })
            messages.success(request, "Your message has been sent successfully!")
            return redirect("/contact/")
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'mainwebsite/contact.html')

def clients(request):
    return render(request, 'mainwebsite/clients.html')
