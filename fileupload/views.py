from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.conf import settings
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .forms import UploadFileForm
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_extension = os.path.splitext(file.name)[1]

            # Process the file based on its extension
            if file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file)
            elif file_extension == '.csv':
                df = pd.read_csv(file)
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Unsupported file format!'})

            # Rename columns to remove spaces
            df.columns = df.columns.str.replace(' ', '_')
            summary = df.groupby(['Cust_State', 'Cust_Pin'])['DPD'].sum().reset_index()

            # Render the email content from the template
            email_content = render_to_string('email_summary.html', {'summary': summary.to_dict(orient='records')})

            # Email details
            subject = f"Python Assignment - Kumar Shivesh"
            recipient_list = settings.RECIPIENT_LIST
            cc_list = settings.CC_LIST

            # Create and send the email with CC
            email = EmailMessage(
                subject,
                email_content,
                settings.EMAIL_HOST_USER,
                recipient_list,
                cc=cc_list
            )
            email.content_subtype = 'html'  # Important: set the content type to HTML
            email.send()

            return render(request, 'summary.html', {'summary': summary.to_dict(orient='records')})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

