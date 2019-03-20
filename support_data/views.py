
from django.views.generic.edit import CreateView, UpdateView
from  django.views.generic.list import ListView


from .models import Organization


class OrganizationCreate(CreateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationUpdate(UpdateView):
    model = Organization
    fields = ['name', 'country']


class OrganizationListView(ListView):
    model = Organization
    paginate_by = 10
