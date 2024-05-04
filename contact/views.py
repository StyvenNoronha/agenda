from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from contact.models import Contact
from django import forms
from django.urls import reverse
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
        first_name = forms.CharField(
            widget=forms.TextInput(
                attrs = {'placeholder':'João'}
            ),
        label='Nome'    
        )
        last_name = forms.CharField(
            widget=forms.TextInput(
                attrs = {'placeholder':'Cunha Neto'}
            ),
            label='Último Nome'
        )
        phone = forms.CharField(
            widget=forms.TextInput(
                attrs = {'placeholder':'(99)99999-9999'}
            ),
            label='Telefone'        
        )
        email = forms.CharField(
            widget=forms.TextInput(
                attrs = {'placeholder':'example@example.com'}
            ),
            label='E-mail'        
        )
        picture = forms.ImageField(
            widget=forms.FileInput(
                attrs={'accept':'image/*'}
            ),
            label='Imagem do contato'
        )
        
        class Meta:
            model = Contact
            fields = ('first_name','last_name','phone','email','description','category','picture')          
def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        context = {'form': form}
        if form.is_valid():
            form.save()
        return redirect('contact:create')
    
    
    context = {'form':ContactForm}
    return render(request,'contact/create.html',context)
def update(request,contact_id):

    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    form_action = reverse('contact:update', args=[contact_id])
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        context = {'form': ContactForm(instance=contact), 'form_action': form_action}
        if form.is_valid():
          contact =  form.save()
        return redirect('contact:update', args=[contact.pk])
    
    
    context = {'form':ContactForm(instance=contact_id), 'form_action': form_action}
    return render(request,'contact/create.html',context)
def delete(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, show=True)
    contact.delete()
    return redirect('contact:index')