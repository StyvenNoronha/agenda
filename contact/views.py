from django.http import Http404
from django.shortcuts import render
from contact.models import Contact
# Create your views here.
def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')[0:10]
    context = {'contacts':contacts,'titulo': 'Contatos - ' }
    return render(request,'contact/index.html',context)



def contact(request, id):
    single_contact = Contact.objects.filter(pk=id,show=True).first()
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'

    if single_contact is None:
        raise Http404()
    
    context = {'contact':single_contact,'titulo':contact_name}
    return render(request,'contact/contact.html',context)
