from typing import Any
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import Q, F
from django.db.models.functions import Coalesce
from itertools import chain
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.template import loader
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from .models import guest_transaction, hotel_guest, person_type
from .models import GQF
from pprint import pprint
from datetime import datetime
import pytz
import openpyxl
from libs.misc import convert_excel_number_to_date
from custom_functions.apps import queryset_label_to_verbose_dict
from sheets.record import GuestRecord, ReservationRecord

# Create your views here.
# def index(request):
#     return render(request, 'accounts/login.html')

@login_required
def reservations(request):
    # listings = guest_transaction.objects.all()
    data = guest_transaction
    field_names = list(data._meta.get_fields())
    titles = [f.verbose_name for f in field_names]
    field_Names = [f.name for f in field_names]
#    field_names = [f.verbose_name for f in guest_transaction._meta.fields if isinstance(f, Model) and f.name != 'reservation_id']
    # data = [[getattr(ins, name) for name in field_Names]
    #         for ins in listings.objects.prefetch_related().all()]
    listings = [[getattr(ins, name) if getattr(ins, name) is not None else '' 
                 for name in field_Names]
            for ins in data.objects.filter(trans_date_checkin__isnull=True).all().order_by('-trans_date_checkin', 'trans_guest_id').values()]

    paginator = Paginator(listings, 10)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    return render(request, 'gms/reservations.html', {'field_names': titles, 'object_data': listings})

@method_decorator(login_required, name='dispatch')
class ReservationListView(ListView):
  model = guest_transaction
  template_name = 'gms/reservations.html'
  context_object_name = 'reservations'

  def get_queryset(self):
    queryset = guest_transaction.objects \
        .filter(trans_date_checkin__isnull=True) \
        .select_related('trans_guest_id') \
        .order_by('trans_date_checkin') \
        .values(
            'trans_date_checkin',
            'trans_room_id__room_name',
            'transaction_id',
            'trans_guest_id',
            'trans_guest_id__guest_passport_number',
            'trans_guest_id__guest_name',
            'trans_guest_id__guest_date_of_birth',
            'trans_guest_id__guest_comm_dweller',
            'trans_guest_id__guest_type',
            'trans_date_checkin_planned',
            'trans_checkin_hotel',
            'trans_remarks',
        )
    return queryset


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Get the object list
    object_list = context['object_list']
    
    # Create a list to store the data for each object
    object_data = []
    
    COLHEAD = queryset_label_to_verbose_dict()
    # print('COLHEAD')
    # pprint(COLHEAD)

    field_names = {}
    qs = self.get_queryset()
    if qs:
      for fld in qs[0].keys():
        fld_name = fld.split('__')[-1] if '__' in fld else fld
        field_names[fld_name] = COLHEAD.get(fld_name) if COLHEAD.get(fld_name) else ''
      
      for obj in qs:
        obj_fields = {}
        for field_name, fld_value in obj.items():
          obj_fields[field_name] = fld_value if fld_value else ''
        object_data.append(obj_fields)

      context['object_data'] = object_data
      context['field_names'] = field_names
    else:
      context['object_data'] = None
      context['field_names'] = None

    # print('field_names')
    # pprint(field_names)

    print('object_data')
    pprint(object_data)
    return context


@login_required
def manual_ingest(request):
  if request.method != 'POST':
    return render(request, 'gms/upload.html')
  
  filename = request.FILES['xlsx_file']

  # Process the uploaded file here
  wb = openpyxl.load_workbook(filename)
  sheet = wb.active
  
  file_data = []
  for row in sheet.rows:
    line = [c.value if c.value is not None else '' for c in row]
    if any(line):                
      file_data.append(line)

  if len(file_data) < 2:
    messages.error(request, 'No relevant data found, please ensure there is at least 1 row of data.')
    return redirect('upload')
    
  file_headers = tuple(file_data[0])
  guest_fields_in_file = []
  data = []

  # Process the upload file row by row
  for row in file_data[1:]:
    # Prepare the guest record and reservation record as a dictionary
    try:
      guest_record = GuestRecord(dict(zip(file_headers, row)))
      reservation_record = ReservationRecord(dict(zip(file_headers, row)))
      message = 'Success: Guest record created; ' if guest_record.created else 'Warning: Guest record found; '
      message += 'Reservation created' if reservation_record.created else 'Reservation found'
    except ValueError as e:
      message = 'Error: ' + str(e)
    finally:
      merged_dict = {**(guest_record.raw_data), **(reservation_record.raw_data)}
      merged_dict['Ingestion results'] = message
      data.append(merged_dict)
      # pprint(data)

  guest_fields_in_file = list(data[0].keys())
  return render(request, 'gms/upload_details.html', {'header':guest_fields_in_file, 'data':data})


@login_required
def process_checkin(request):
  if request.method == 'POST':
    transaction_id = request.POST.get('transaction_id')
    if transaction_id == '':
      messages.error(request, 'Transaction ID not found')
      return redirect('reservations')  # Replace 'error-page' with the appropriate URL or view name
    
    # Retrieve the guest transaction record
    try:
      transaction = guest_transaction.objects.get(transaction_id=transaction_id)
    except guest_transaction.DoesNotExist:
      # Handle the case when the transaction does not exist
      messages.error(request, 'Reservation does not exist!')
      return redirect('reservations')  # Replace 'error-page' with the appropriate URL or view name
    
    # Update the trans_date_checkin field with the current timestamp
    transaction.trans_date_checkin = datetime.now(pytz.utc)
    transaction.save()
    
    # Redirect to a success page or do any other desired action
    return redirect('reservations')  # Replace 'success-page' with the appropriate URL or view name
  
  # If the request method is not POST, render the form template as usual
  return render(request, 'gms/reservations.html')

@login_required
def search_checkin(request):
  if request.method == 'POST':
    id_or_name = request.POST.get('id_or_name')
    qs = guest_transaction.objects \
        .filter(trans_date_checkin__isnull=True) \
        .select_related('trans_guest_id') \
        .order_by('trans_date_checkin') \
        .values(
            'trans_date_checkin',
            'trans_room_id__room_name',
            'transaction_id',
            'trans_guest_id',
            'trans_guest_id__guest_passport_number',
            'trans_guest_id__guest_name',
            'trans_guest_id__guest_date_of_birth',
            'trans_guest_id__guest_comm_dweller',
            'trans_guest_id__guest_type',
            'trans_date_checkin_planned',
            'trans_checkin_hotel',
            'trans_remarks',
        )
    if id_or_name:
      qs = qs.filter(
        Q(trans_guest_id__guest_id__icontains=id_or_name) |
        Q(trans_guest_id__guest_name__icontains=id_or_name)
        )
    # Create a list to store the data for each object
    context = {'user_input':request.POST}
    field_names = {}
    object_data = []
    
    COLHEAD = queryset_label_to_verbose_dict()
    # print('COLHEAD')
    # pprint(COLHEAD)


    if qs:
      for fld in qs[0].keys():
        fld_name = fld.split('__')[-1] if '__' in fld else fld
        field_names[fld_name] = COLHEAD.get(fld_name) if COLHEAD.get(fld_name) else ''
      
      for obj in qs:
        obj_fields = {}
        for field_name, fld_value in obj.items():
          obj_fields[field_name] = fld_value if fld_value else ''
        object_data.append(obj_fields)

      context['object_data'] = object_data
      context['field_names'] = field_names
    else:
      context['object_data'] = None
      context['field_names'] = None

    # print('field_names')
    # pprint(field_names)

    # print('object_data')
    # pprint(object_data)
    return render(request, 'gms/reservations.html', context)


@login_required
def dashboard(request):
  # Get the count of guest_transaction records that have not checked in
  not_checked_in_count = guest_transaction.objects.filter(trans_date_checkout__isnull=True).count()
  puq_ingested = guest_transaction.objects.filter(Q(trans_guest_id__guest_type__exact='Guest') &
                                                      Q(trans_date_checkin__isnull=True) &
                                                      Q(trans_room_id__isnull=True)
                                                      ).count()
  non_puq_inserted = 0
  non_puq = 0
  non_puq_assigned = 0
  non_puq_checked_in = 0
  drop_cases = 0
  moh_cases = 0
  puq_assigned = 0
  puq_checked_in = 0

  context = {
     'drop_cases'        : drop_cases,
     'moh_cases'         : moh_cases,
     'non_puq'           : non_puq,
     'non_puq_inserted'  : non_puq_inserted,
     'non_puq_assigned'  : non_puq_assigned,
     'non_puq_checked_in': non_puq_checked_in,
     'all_puq'           : not_checked_in_count,
     'puq_ingested'      : puq_ingested,
     'puq_assigned'      : puq_assigned,
     'puq_checkedin'     : puq_checked_in,
  }

  return render(request, 'gms/dashboard.html', context)

@login_required
def upload(request):
  return render(request, 'gms/upload.html')