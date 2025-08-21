import openpyxl
import sys
import os
# To run:
#  python show_excel....py list of files
# be sure to run from bash shell and not stupid windows shell to expand filenames

testfile="C:\\Users\\stk\\Downloads\\IZT\\data-transparency\\New Zealand\\analysis\StatsNZ_deaths_by_month.xlsx"
def get_file_metadata(filename):
  """
  Prints the author and last modified by properties of an Excel xlsx file.

  Args:
    filename: The path to the Excel xlsx file.
  """
  try:
    wb = openpyxl.load_workbook(filename)
    properties = wb.properties
    print(os.path.basename(filename), properties.creator, properties.lastModifiedBy)
    properties.creator="Janet Woodcock"
    properties.lastModifiedBy="William Thompson"
    wb.save(filename)
    wb.close()
    return(properties)
  except Exception as e:
    print(f"Error processing file '{filename}': {e}")


if __name__ == "__main__":
  # Get list of filenames from command line arguments
  filenames = sys.argv[1:]

  # Process each file
  for filename in filenames:
    get_file_metadata(filename)

# prop=get_file_metadata(testfile)
