from django.shortcuts import render, redirect
from .forms import ApplicationFrom
from .models import Form
from django.contrib import messages
from django.core.mail import EmailMessage

ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_uploaded_file(f):
    with open(f'resumes/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    # if this is a POST request
    if request.method == 'POST':
        # create a form object
        form = ApplicationFrom(request.POST, request.FILES)
        if form.is_valid():
            # get the information from the webpage
            first_name = form.cleaned_data['first_name'].title()
            last_name = form.cleaned_data['last_name'].title()
            email = form.cleaned_data['email']
            start_date = form.cleaned_data['start_date']
            occupation = form.cleaned_data['occupation']

            if request.FILES["resume"] and allowed_files(request.FILES["resume"].name):
                handle_uploaded_file(request.FILES["resume"])

                # store it into the database
                Form.objects.create(first_name=first_name, last_name=last_name, email=email,
                                    start_date=start_date, occupation=occupation, resume=request.FILES["resume"].name)

                # email the user
                body = f"{first_name}, Your application was submitted successfully,\n" \
                       f"Here are you data: \n{first_name}\n{last_name}\n{start_date}\n{occupation}\n" \
                       "If it's a fit we will contact you,\n" \
                       "Thank you for your time."

                email = EmailMessage(subject='Application Submitted Successfully',
                                     body=body, to=[email])
                email.send()

                # display the user a success message
                messages.success(request, 'Your application has been submitted successfully!')
            else:
                # display the user error message
                messages.warning(request, 'Resume file type is not allowed.\n'
                                          f'Please provide those types only: {ALLOWED_EXTENSIONS}')

                # return the form so the user will not need to type the data again
                return render(request, 'index.html', {'form': form})
    # if this is a GET request
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')
