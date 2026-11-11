import os
import re
import json
import random
import joblib
import nltk

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from nltk.corpus import stopwords

# Import all forms and models
from .forms import *
from .models import *

# ==============================================================================
# ─── MACHINE LEARNING SETUP (Fake Job Detector) ───────────────────────────────
# ==============================================================================

nltk.download("stopwords", quiet=True)
STOP_WORDS = set(stopwords.words("english"))

# Attempt to load the model securely at startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

try:
    MODEL = joblib.load(MODEL_PATH)
    print("✅ Fake Job Detector model loaded successfully.")
except Exception as e:
    print(f"⚠️ Model load warning: {e}. Please ensure model.pkl exists.")
    MODEL = None


def clean_text(text: str) -> str:
    """Clean text for ML prediction."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(tokens)


# ==============================================================================
# ─── PUBLIC PAGES ─────────────────────────────────────────────────────────────
# ==============================================================================

def index(request):
    return render(request, 'index.html', {})


def about(request):
    return render(request, 'about.html', {})


def menu(request):
    return render(request, 'menu.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank You For Contacting Us...!')
            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your submission.')
    return render(request, 'contact.html')


# ==============================================================================
# ─── FAKE JOB DETECTOR API ────────────────────────────────────────────────────
# ==============================================================================

def fake_job_detector(request):
    """Render the Fake Job Detector page."""
    return render(request, 'fake_job_detector.html')


@csrf_exempt
def predict_job(request):
    """Accept POST with job details JSON, return fake/real prediction."""
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    if MODEL is None:
        return JsonResponse(
            {"error": "Model not loaded. Please ensure model.pkl exists."}, status=500
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    title = data.get("title", "")
    company = data.get("company", "")
    description = data.get("description", "")
    requirements = data.get("requirements", "")
    benefits = data.get("benefits", "")
    location = data.get("location", "")
    salary = data.get("salary", "")

    combined = f"{title} {company} {description} {requirements} {benefits} {location} {salary}"
    cleaned = clean_text(combined)

    if not cleaned.strip():
        return JsonResponse(
            {"error": "Please fill in at least the Job Title and Description."}, status=400
        )

    try:
        prediction = MODEL.predict([cleaned])[0]
        proba = MODEL.predict_proba([cleaned])[0]

        fake_pct = round(float(proba[1]) * 100, 1)
        real_pct = round(float(proba[0]) * 100, 1)

        if fake_pct >= 70:
            risk = "high"
        elif fake_pct >= 40:
            risk = "medium"
        else:
            risk = "low"

        return JsonResponse({
            "prediction": int(prediction),
            "label": "FAKE" if prediction == 1 else "REAL",
            "fake_pct": fake_pct,
            "real_pct": real_pct,
            "risk": risk
        })

    except Exception as e:
        return JsonResponse({"error": f"Prediction failed: {str(e)}"}, status=500)


# ==============================================================================
# ─── ADMIN DASHBOARD ──────────────────────────────────────────────────────────
# ==============================================================================

def admin_index(request):
    return render(request, 'admin_index.html', {})


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Admin.objects.get(email=email, password=password)
            request.session['email'] = user.email
            return redirect('admin_index')
        except Admin.DoesNotExist:
            return render(request, 'admin_login.html', {'error': "Invalid email or password"})
    return render(request, 'admin_login.html')


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


def admin_addnotification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification added successfully!')
            return redirect('admin_addnotification')
        else:
            form = NotificationForm()
        return render(request, 'admin_addnotification.html', {'form': form})
    return render(request, 'admin_addnotification.html')


def admin_viewnotification(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'admin_viewnotification.html', {'notifications': notifications})


def delete_notification(request, id):
    try:
        notification = Notification.objects.get(id=id)
        notification.delete()
    except Notification.DoesNotExist:
        pass
    return redirect('admin_viewnotification')


def admin_viewcontact(request):
    contacts = Contact.objects.all().order_by('-id')
    return render(request, 'admin_viewcontact.html', {'contacts': contacts})


def admin_password(request):
    email = request.session.get('email')
    if not email:
        return redirect('admin_login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            customer = Admin.objects.get(email=email, password=old_password)
            if new_password != confirm_password:
                return render(request, 'admin_password.html', {"msg": "New password and confirm password do not match"})
            if old_password == new_password:
                return render(request, 'admin_password.html',
                              {"msg": "New password and old password must not be same."})

            customer.password = new_password
            customer.save()
            return render(request, 'admin_login.html', {"msg": "Password Changed Successfully!"})
        except Admin.DoesNotExist:
            return render(request, 'admin_password.html', {"msg": "User does not exist"})
    return render(request, 'admin_password.html', {"email": email})


def admin_viewcustomer(request):
    con = CustomerRegi.objects.all().order_by('-id')
    return render(request, 'admin_viewcustomer.html', {'con': con})


def accept_customer(request, id):
    customer = CustomerRegi.objects.get(id=id)
    customer.status = 'Accepted'
    customer.save()
    messages.success(request, f"Customer {customer.name} has been approved and can now log in.")
    return redirect('admin_viewcustomer')


def reject_customer(request, id):
    customer = CustomerRegi.objects.get(id=id)
    customer.status = 'Rejected'
    customer.save()
    messages.warning(request, f"Customer {customer.name}'s registration request was rejected.")
    return redirect('admin_viewcustomer')


def admin_viewjobprovider(request):
    con = JobProvider.objects.all().order_by('-id')
    return render(request, 'admin_viewjobprovider.html', {'con': con})


def accept_jobprovider(request, id):
    provider = JobProvider.objects.get(id=id)
    provider.status = 'Accepted'
    provider.save()
    messages.success(request, f"Job Provider {provider.name} has been approved and can now log in.")
    return redirect('admin_viewjobprovider')


def reject_jobprovider(request, id):
    provider = JobProvider.objects.get(id=id)
    provider.status = 'Rejected'
    provider.save()
    messages.warning(request, f"Job Provider {provider.name}'s registration request was rejected.")
    return redirect('admin_viewjobprovider')


# ==============================================================================
# ─── CUSTOMER VIEWS ───────────────────────────────────────────────────────────
# ==============================================================================

def customer_index(request):
    return render(request, 'customer_index.html', {})


def customer_regi(request):
    if request.method == "POST":
        form = CustomerRegiForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            if CustomerRegi.objects.filter(email=email).exists():
                return render(request, 'customer_regi.html', {
                    'form': form,
                    'msg': 'Account with this email already exists. Please login.'
                })
            customer = form.save(commit=False)
            customer.password = make_password(form.cleaned_data['password'])
            customer.save()

            subject = "Welcome to Fratello! Registration Received"
            message = f"""
            Dear {customer.name},

            🎉 Thanks for registering with us! 🎉
            We have successfully received your registration request.

            Please note: Your account is currently pending admin approval.
            Once our team verifies your details, you will be able to log in and start shopping.

            Regards,
            Team Fratello
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [customer.email], fail_silently=False)
            return render(request, 'customer_login.html', {
                'msg': 'Successfully Registered! Please wait for admin approval before logging in.'
            })
        else:
            print("Form Errors:", form.errors)
    else:
        form = CustomerRegiForm()
    return render(request, 'customer_regi.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomerRegi.objects.get(email=email)
            if check_password(password, user.password):
                if user.status == 'Accepted':
                    otp = str(random.randint(100000, 999999))
                    request.session['pre_otp_email'] = user.email
                    request.session['otp'] = otp

                    subject = "Your Login OTP for Fratello"
                    message = f"""
                    Dear {user.name},

                    Your One-Time Password (OTP) for login is: {otp}

                    Please do not share this password with anyone.
                    If you did not request this, please ignore this email.

                    Regards,
                    Team Fratello
                    """
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    return redirect('customer_otp_verify')
                elif user.status == 'Rejected':
                    return render(request, 'customer_login.html',
                                  {'error': "Your account registration was rejected by the admin."})
                else:
                    return render(request, 'customer_login.html',
                                  {'error': "Your account is pending admin approval. Please check back later."})
            else:
                return render(request, 'customer_login.html', {'error': "Invalid email or password"})
        except CustomerRegi.DoesNotExist:
            return render(request, 'customer_login.html', {'error': "Invalid email or password"})
    return render(request, 'customer_login.html')


def customer_otp_verify(request):
    if 'pre_otp_email' not in request.session:
        return redirect('customer_login')
    email = request.session.get('pre_otp_email')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            request.session['email'] = email
            del request.session['otp']
            del request.session['pre_otp_email']
            return redirect('customer_index')
        else:
            return render(request, 'customer_otp_verify.html',
                          {'error': 'Invalid OTP. Please try again.', 'email': email})
    return render(request, 'customer_otp_verify.html', {'email': email})


def customer_viewnotification(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'customer_viewnotification.html', {'notifications': notifications})


def customer_changepassword(request):
    email = request.session.get('email')
    if not email:
        return redirect('customer_login')
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            customer = CustomerRegi.objects.get(email=email)
            if not check_password(old_password, customer.password):
                return render(request, 'customer_changepassword.html', {"msg": "Current password is incorrect"})
            if new_password != confirm_password:
                return render(request, 'customer_changepassword.html',
                              {"msg": "New password and confirm password do not match"})
            if old_password == new_password:
                return render(request, 'customer_changepassword.html',
                              {"msg": "New password and old password must not be same."})

            customer.password = make_password(new_password)
            customer.save()
            return render(request, 'customer_login.html', {"msg": "Password Changed Successfully!"})
        except CustomerRegi.DoesNotExist:
            return render(request, 'customer_changepassword.html', {"msg": "System error: User record not found"})
    return render(request, 'customer_changepassword.html', {"email": email})


def customer_profile(request):
    customer_email = request.session.get('email')
    if not customer_email:
        return redirect('customer_login')
    profile = get_object_or_404(CustomerRegi, email=customer_email)
    return render(request, 'customer_profile.html', {'user': profile})


def customer_editprofile(request):
    session_email = request.session.get('email')
    if not session_email:
        return redirect('customer_login')
    customer = CustomerRegi.objects.get(email=session_email)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.mobile = request.POST.get('mobile')
        customer.pincode = request.POST.get('pincode')
        customer.address = request.POST.get('address')
        try:
            customer.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('customer_profile')
        except Exception as e:
            return render(request, 'customer_editprofile.html', {'user': customer, 'msg': 'Error updating profile.'})

    return render(request, 'customer_editprofile.html', {'user': customer})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            customer = CustomerRegi.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['forgot_otp'] = str(otp)
            request.session['reset_email'] = email

            subject = 'Password Reset OTP - Appatizer'
            message = f'Hello {customer.name},\n\nYour OTP for password reset is: {otp}\n\nDo not share this with anyone.'
            recipient_list = [email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            messages.success(request, 'An OTP has been sent to your registered email.')
            return redirect('forgot_otp_verify')
        except CustomerRegi.DoesNotExist:
            messages.error(request, 'This email is not registered with us!')
            return redirect('forgot_password')
    return render(request, 'customer_forgot_password.html')


def forgot_otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('forgot_otp')
        if entered_otp == session_otp:
            messages.success(request, 'OTP verified successfully. Please enter your new password.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('forgot_otp_verify')
    return render(request, 'customer_forgot_otp_verify.html')


def reset_password(request):
    if 'reset_email' not in request.session:
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if new_password == confirm_password:
            try:
                customer = CustomerRegi.objects.get(email=email)
                customer.password = make_password(new_password)
                customer.save()
                del request.session['forgot_otp']
                del request.session['reset_email']
                messages.success(request, 'Password reset successfully! You can now login.')
                return redirect('customer_login')
            except CustomerRegi.DoesNotExist:
                messages.error(request, 'Something went wrong!')
                return redirect('forgot_password')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')

    return render(request, 'customer_reset_password.html')

def customer_viewjobs(request):
    jobs=JobPosting.objects.all()
    return render(request, 'customer_viewjobs.html', {'jobs': jobs})

def customer_jobdetails(request, id):
    job = get_object_or_404(JobPosting, pk=id)
    return render(request, 'customer_jobdetails.html', {'job': job})


def customer_apply_job(request, id):
    # 1. Ensure the customer is securely logged in
    email = request.session.get('email')
    if not email:
        messages.warning(request, "Please log in to apply for jobs.")
        return redirect('customer_login')

    # 2. Get the specific Customer and Job objects
    customer = CustomerRegi.objects.get(email=email)
    job = get_object_or_404(JobPosting, id=id)

    # 3. Check if the customer has ALREADY applied to this specific job
    if JobApplication.objects.filter(job=job, applicant=customer).exists():
        messages.warning(request, f"You have already applied for the {job.title} position.")
        return redirect('customer_viewjobs')

    if request.method == 'POST':
        # request.FILES is required because we are uploading a resume!
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save temporarily
            application = form.save(commit=False)

            # Link the application to the specific job and customer
            application.job = job
            application.applicant = customer

            # Save to database
            application.save()

            messages.success(request, f"Successfully applied for {job.title}!")
            return redirect('customer_viewjobs')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobApplicationForm()

    return render(request, 'customer_apply_job.html', {'form': form, 'job': job})


def customer_my_applications(request):
    # Ensure the customer is logged in
    email = request.session.get('email')
    if not email:
        return redirect('customer_login')
    # Get the logged-in customer
    customer = CustomerRegi.objects.get(email=email)

    # Fetch all their job applications, newest first
    applications = JobApplication.objects.filter(applicant=customer).order_by('-applied_at')

    return render(request, 'customer_my_applications.html', {'applications': applications})

# ==============================================================================
# ─── JOB PROVIDER VIEWS ───────────────────────────────────────────────────────
# ==============================================================================

def jobprovider_index(request):
    if 'jp_email' not in request.session:
        return redirect('jobprovider_login')
    return render(request, 'jobprovider_index.html')


def jobprovider_regi(request):
    if request.method == 'POST':
        form = JobProviderForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if JobProvider.objects.filter(email=email).exists():
                return render(request, 'jobprovider_regi.html',
                              {'form': form, 'msg': 'Account already exists! Please Login'})

            jobprovider = form.save(commit=False)
            jobprovider.password = make_password(form.cleaned_data.get('password'))
            jobprovider.save()

            subject = "Welcome to Fratello! Registration Received"
            message = f"""
            Dear {jobprovider.name},

            🎉 Thanks for registering as a Job Provider! 🎉
            We have successfully received your registration request.

            Please note: Your account is currently pending admin approval.
            Once our team verifies your details, you will be able to log in.

            Regards,
            Team Fratello
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [jobprovider.email], fail_silently=False)

            return render(request, 'jobprovider_login.html', {
                'msg': 'Successfully Registered! Please wait for admin approval before logging in.'
            })
    else:
        form = JobProviderForm()

    return render(request, 'jobprovider_regi.html', {'form': form})


def jobprovider_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = JobProvider.objects.get(email=email)

            if check_password(password, user.password):
                if user.status == 'Accepted':
                    otp = str(random.randint(100000, 999999))
                    request.session['jp_pre_otp_email'] = user.email
                    request.session['jp_otp'] = otp

                    subject = "Your Job Provider Login OTP"
                    message = f"""
                    Dear {user.name},

                    Your One-Time Password (OTP) for login is: {otp}

                    Please do not share this password with anyone.

                    Regards,
                    Team Fratello
                    """
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    return redirect('jobprovider_otp_verify')

                elif user.status == 'Rejected':
                    return render(request, 'jobprovider_login.html',
                                  {'error': "Your account registration was rejected by the admin."})
                else:
                    return render(request, 'jobprovider_login.html',
                                  {'error': "Your account is pending admin approval. Please check back later."})
            else:
                return render(request, 'jobprovider_login.html', {'error': "Invalid email or password"})

        except JobProvider.DoesNotExist:
            return render(request, 'jobprovider_login.html', {'error': "Invalid email or password"})

    return render(request, 'jobprovider_login.html')


def jobprovider_otp_verify(request):
    if 'jp_pre_otp_email' not in request.session:
        return redirect('jobprovider_login')

    email = request.session.get('jp_pre_otp_email')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('jp_otp')

        if entered_otp == stored_otp:
            request.session['jp_email'] = email
            del request.session['jp_otp']
            del request.session['jp_pre_otp_email']
            return redirect('jobprovider_index')
        else:
            return render(request, 'jobprovider_otp_verify.html',
                          {'error': 'Invalid OTP. Please try again.', 'email': email})

    return render(request, 'jobprovider_otp_verify.html', {'email': email})


def jobprovider_viewnotification(request):
    if 'jp_email' not in request.session:
        return redirect('jobprovider_login')
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'jobprovider_viewnotification.html', {'notifications': notifications})


def jobprovider_changepassword(request):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            jp = JobProvider.objects.get(email=email)
            if not check_password(old_password, jp.password):
                return render(request, 'jobprovider_changepassword.html', {"msg": "Current password is incorrect"})

            if new_password != confirm_password:
                return render(request, 'jobprovider_changepassword.html',
                              {"msg": "New password and confirm password do not match"})

            if old_password == new_password:
                return render(request, 'jobprovider_changepassword.html',
                              {"msg": "New password and old password must not be the same."})

            jp.password = make_password(new_password)
            jp.save()
            return render(request, 'jobprovider_login.html',
                          {"msg": "Password Changed Successfully! Please log in again."})

        except JobProvider.DoesNotExist:
            return render(request, 'jobprovider_changepassword.html', {"msg": "System error: User record not found"})

    return render(request, 'jobprovider_changepassword.html', {"email": email})


def jobprovider_profile(request):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    profile = get_object_or_404(JobProvider, email=email)
    return render(request, 'jobprovider_profile.html', {'user': profile})


def jobprovider_editprofile(request):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    jp = JobProvider.objects.get(email=email)

    if request.method == 'POST':
        jp.name = request.POST.get('name')
        jp.mobile = request.POST.get('mobile')
        jp.address = request.POST.get('address')

        try:
            jp.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('jobprovider_profile')
        except Exception as e:
            return render(request, 'jobprovider_editprofile.html', {'user': jp, 'msg': 'Error updating profile.'})

    return render(request, 'jobprovider_editprofile.html', {'user': jp})


def jobprovider_addjob(request):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.provider = provider
            job.save()

            messages.success(request, 'Job posted successfully!')
            return redirect('jobprovider_index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobPostingForm()

    return render(request, 'jobprovider_addjob.html', {'form': form})


def jobprovider_viewjobs(request):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)
    jobs = JobPosting.objects.filter(provider=provider).order_by('-created_at')

    return render(request, 'jobprovider_viewjobs.html', {'jobs': jobs})


def jobprovider_jobdetails(request, id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)
    job = get_object_or_404(JobPosting, id=id, provider=provider)

    return render(request, 'jobprovider_jobdetails.html', {'job': job})


def jobprovider_editjobs(request, id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)
    job = get_object_or_404(JobPosting, id=id, provider=provider)

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company_name = request.POST.get('company_name')
        job.location = request.POST.get('location')
        job.salary_range = request.POST.get('salary_range')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.benefits = request.POST.get('benefits')

        try:
            job.save()
            messages.success(request, 'Job Updated Successfully!')
            return redirect('jobprovider_viewjobs')
        except Exception as e:
            return render(request, 'jobprovider_editjobs.html', {'job': job, 'msg': f"Error: {e}"})

    return render(request, 'jobprovider_editjobs.html', {'job': job})


def jobprovider_deletejob(request, id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)
    job = get_object_or_404(JobPosting, id=id, provider=provider)
    job.delete()

    messages.success(request, 'Job posting deleted successfully!')
    return redirect('jobprovider_viewjobs')


def jobprovider_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            provider = JobProvider.objects.get(email=email)
            otp = random.randint(100000, 999999)

            request.session['jp_forgot_otp'] = str(otp)
            request.session['jp_reset_email'] = email

            subject = 'Password Reset OTP - Appatizer (Provider)'
            message = f'Hello {provider.name},\n\nYour OTP for password reset is: {otp}\n\nDo not share this with anyone.'
            recipient_list = [email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            messages.success(request, 'An OTP has been sent to your registered email.')
            return redirect('jobprovider_forgot_otp_verify')

        except JobProvider.DoesNotExist:
            messages.error(request, 'This email is not registered with us as a Job Provider!')
            return redirect('jobprovider_forgot_password')

    return render(request, 'jobprovider_forgot_password.html')


def jobprovider_forgot_otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('jp_forgot_otp')

        if entered_otp == session_otp:
            messages.success(request, 'OTP verified successfully. Please enter your new password.')
            return redirect('jobprovider_reset_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('jobprovider_forgot_otp_verify')

    return render(request, 'jobprovider_forgot_otp_verify.html')


def jobprovider_reset_password(request):
    if 'jp_reset_email' not in request.session:
        return redirect('jobprovider_forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('jp_reset_email')

        if new_password == confirm_password:
            try:
                provider = JobProvider.objects.get(email=email)
                provider.password = make_password(new_password)
                provider.save()

                del request.session['jp_forgot_otp']
                del request.session['jp_reset_email']

                messages.success(request, 'Password reset successfully! You can now login.')
                return redirect('jobprovider_login')
            except JobProvider.DoesNotExist:
                messages.error(request, 'Something went wrong!')
                return redirect('jobprovider_forgot_password')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('jobprovider_reset_password')

    return render(request, 'jobprovider_reset_password.html')


def jobprovider_viewapplication(request, job_id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    # Get the provider to ensure they own this job
    provider = JobProvider.objects.get(email=email)

    # Get the specific job posting
    job_posting = get_object_or_404(JobPosting, id=job_id, provider=provider)

    # Filter ALL applications for this specific job
    applications = JobApplication.objects.filter(job=job_posting).order_by('-applied_at')

    return render(request, 'jobprovider_viewapplication.html', {
        'job_posting': job_posting,
        'applications': applications
    })


def jobprovider_accept_application(request, app_id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    # Get the logged-in provider
    provider = JobProvider.objects.get(email=email)

    # Securely fetch the application using your JobApplication model
    # job__provider=provider ensures that a provider can't accept an application for someone else's job!
    application = get_object_or_404(JobApplication, id=app_id, job__provider=provider)

    # Update the status field in your model
    application.status = 'Accepted'
    application.save()

    # Send an automated email to the Customer
    subject = f"Application Update: {application.job.title}"
    message = f"""
    Dear {application.applicant.name},

    Great news! Your application for the "{application.job.title}" position has been ACCEPTED by {provider.name}.

    They will be in touch with you shortly regarding the next steps.

    Regards,
    Team Appetizer
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER, [application.applicant.email], fail_silently=True)

    messages.success(request, f"You have accepted {application.applicant.name}'s application!")

    # Redirect back to the applications list for this specific job
    return redirect('jobprovider_viewapplication', job_id=application.job.id)


def jobprovider_reject_application(request, app_id):
    email = request.session.get('jp_email')
    if not email:
        return redirect('jobprovider_login')

    provider = JobProvider.objects.get(email=email)

    application = get_object_or_404(JobApplication, id=app_id, job__provider=provider)

    # Update the status field to Rejected
    application.status = 'Rejected'
    application.save()

    subject = f"Application Update: {application.job.title}"
    message = f"""
    Dear {application.applicant.name},

    Thank you for applying to the "{application.job.title}" position at {provider.name}.

    Unfortunately, they have decided to move forward with other candidates at this time. We wish you the best of luck in your job search!

    Regards,
    Team Appetizer
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER, [application.applicant.email], fail_silently=True)

    messages.warning(request, f"You have rejected {application.applicant.name}'s application.")

    return redirect('jobprovider_viewapplication', job_id=application.job.id)