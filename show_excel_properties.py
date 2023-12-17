import openpyxl
import sys

def get_file_metadata(filename):
  """
  Prints the author and last modified by properties of an Excel xlsx file.

  Args:
    filename: The path to the Excel xlsx file.
  """
  try:
    wb = load_workbook(filename)
    properties = wb.properties

    if "creator" in properties:
      print(f"Author: {properties['creator']}")
    else:
      print("Author information not found.")

    if "lastModifiedBy" in properties:
      print(f"Last modified by: {properties['lastModifiedBy']}")
    else:
      print("Last modified by information not found.")

    wb.close()
  except Exception as e:
    print(f"Error processing file '{filename}': {e}")


if __name__ == "__main__":
  # Get list of filenames from command line arguments
  filenames = sys.argv[1:]

  # Process each file
  for filename in filenames:
    get_file_metadata(filename)
