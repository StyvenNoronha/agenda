from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from contact.models import Contact
from django import forms
# Create your views here.





def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - '
    }

    return render(
        request,
        'contact/index.html',
        context
    )
def search(request):
    search_value = request.GET.get('q','').strip()
    if search_value == '':
        return redirect ('contact:index')

    contacts = Contact.objects.filter(show=True).filter(Q(first_name__icontains=search_value)|Q(last_name__icontains=search_value)|Q(phone__icontains=search_value)|Q(email__icontains=search_value)).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {'page_obj':page_obj,'titulo': 'Procura - ' }
    return render(request,'contact/index.html',context)
def contact(request, id):

    single_contact = Contact.objects.filter(pk=id,show=True).first()
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'

    if single_contact is None:
        raise Http404()
    
    context = {'contact':single_contact,'titulo':contact_name}
    return render(request,'contact/contact.html',context)


#formulario
class ContactForm(forms.ModelForm):
        class Meta:
            model = Contact
            fields = ('first_name','last_name','phone','email',)
###############          











def create(request):
    if request.method == 'POST':
        context = {'form':ContactForm(request.POST)}
        return render(request,'contact/create.html',context)
    
    
    context = {'form':ContactForm}
    return render(request,'contact/create.html',context)
