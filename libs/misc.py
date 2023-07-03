from datetime import datetime, timedelta, date as date

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
