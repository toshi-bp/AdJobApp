from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UpoadFileForm

from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UpoadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #ファイルが保存された時
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('success/url')
        else:
            form = UpoadFileForm()
        return render(request, 'upload.html', {'form': form})