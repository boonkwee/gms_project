from datetime import datetime, timedelta, date as date
import re

def running_test(test_func):
  def wrapper(*args, **kwargs):
    print(f"\n\nRunning test: {test_func.__name__}")
    return test_func(*args, **kwargs)
  return wrapper

def convert_excel_number_to_date(excel_number):
  if isinstance(excel_number, datetime):
    return excel_number.date()
  elif isinstance(excel_number, date):
    return excel_number
  elif isinstance(excel_number, int):
    return convert_excel_number_to_datetime(excel_number).date()

def convert_excel_number_to_datetime(excel_number):
  try:
    # Define the base date in Excel (January 1, 1900)
    base_date = datetime(1900, 1, 1)

    # Calculate the number of days to add to the base date
    delta = timedelta(days=excel_number - 2)  # Subtracting 2 because of Excel's date system

    # Convert the Excel number to a date
    date = base_date + delta

    return date

  except ValueError as ve:
    # Handle specific ValueError when excel_number is not a valid integer or float
    print("Error: excel_number must be a valid integer or float.")
    return None

  except Exception as e:
    # Handle any other exceptions that may occur during the conversion
    print("Error occurred while converting Excel number to date:", str(e))
    return None


def NRIC_checksum(nric=None):
    '''
    https://userapps.support.sap.com/sap/support/knowledge/en/2572734
    '''
    if nric is None:
        raise ValueError("Missing NRIC for verification")
    elif not isinstance(nric, str):
        raise ValueError(str(type(nric)) + " given, expected NRIC as string")
    l_nric = str.lower(nric)
    if re.match(string=l_nric, pattern="^[mstgf]{1}\\d{7}[abcdefghijklmnpqrtuwxz]{1}$") is None:
        return False
    prefix = l_nric[0]
    
    suffix = l_nric[-1]
    offset = 4 if prefix in "tg" else 3 if prefix in "m" else 0
    vector_m = [int(i) for i in "2765432"]
    vector_o = [int(i) for i in l_nric[1:-1]]
    displacement = (sum(map(lambda x: x[0]*x[1], zip(vector_m, vector_o))) + offset) % 11
    # pprint(displacement)
    return suffix == "xwutrqpnmlk"[displacement] if prefix in "gfm" else suffix == "jzihgfedcba"[displacement]