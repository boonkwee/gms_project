from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import loader
from .models import hotel_guest

# Create your views here.
@method_decorator(login_required, name='dispatch')
def view_guests(request):
  guest_list = hotel_guest.objects.all()
  template = loader.get_template('guests/guestlist.html')
  context = {
    'guest_list' : guest_list
  }
  # return render(request, 'guests/guestlist.html', context=context)
  return template.render(context, request)

@method_decorator(login_required, name='dispatch')
class GuestListView(ListView):
  model = hotel_guest
  template_name = 'guests/guestlist.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Get the object list
    object_list = context['object_list']
    
    # Create a list to store the data for each object
    object_data = []
    
    # Get the field names of each object
    field_names = []

    if object_list:
      for obj in object_list:
        # Get the field names and corresponding values for the object
        obj_fields = [getattr(obj, field.name) if getattr(obj, field.name) is not None else ''
                      for field in obj._meta.get_fields() if not field.is_relation]
        # obj_fields = [(field.name, getattr(obj, field.name)) for field in obj._meta.get_fields()]
        
        # Add the object's data to the object_data list
        object_data.append(obj_fields)
            
        # obj_field_names = [field.verbose_name for field in obj._meta.get_fields() if not field.is_relation]
        # field_names.extend(obj_field_names)
        field_names = [field.verbose_name for field in obj._meta.get_fields() if not field.is_relation]
    
      context['object_data'] = object_data
      context['field_names'] = field_names
    else:
      context['object_data'] = None
      context['field_names'] = None

    return context