import requests
import lxml
from lxml.html import parse
import csv
import sys
GOOGLE_URL = "http://www.google.com/search?q="
IN_FILE_PATH = "/home/wesley/Downloads/d3schools.csv"
OUT_FILE_PATH = "/home/wesley/Downloads/scraper_result.csv"

def main():
    """ 
    Take an input csv file with College names as each row, and outputs 
    a file with the college name, the google search result title, and
    the google search result link as the rows

    Syntax:
    >> python scraper.py /path/to/input.csv /path/to/output.csv

    Otherwise, IN_FILE_PATH and OUT_FILE_PATH are the defaults for 
    the location/names of the input/output csv
    """
    try:
        # try to get the file input/output from sys.argv
        IN_FILE_PATH = sys.argv[1] # first arg is the input file
        OUT_FILE_PATH = sys.argv[2] # second arg is the output file
    except KeyError:
        print "To enter filepaths from console, use the following syntax >> python scraper.py /path/to/input.csv /path/to/output.csv"
    rows = get_athletic_sites_from_file(IN_FILE_PATH)
    write_athletic_sites_to_file(OUT_FILE_PATH, rows)

def get_athletic_sites_from_file(fpath):
    reader = csv.reader(open(fpath, "rb"))
    rows = [ [row[0]] for row in reader]
    for row in rows:
        print row[0] # show which school is being done
        row.extend(get_athletics_site(row[0]))
        print row # output of google search
    return rows

def write_athletic_sites_to_file(fpath, iterable):
    writer = csv.writer(open(fpath, "wb"))
    for row in iterable:
        print row
        try:
            writer.writerow(row)
        except UnicodeEncodeError:
            print "THERE WAS A UNICODE ERROR FOR %s" %str(row)
            writer.writerow([row[0],"",row[2]]) # most of the unicode errors are a result of the Google Search Result Title, so replace it with empty string
        print "row written."
    # writer.writerows(iterable)

def get_athletics_site(school_name):
    search_query = school_name + " athletics"
    return get_top_google_result(search_query)

def get_google_results(search_query):
    search_url = GOOGLE_URL + search_query
    doc = parse(search_url).getroot()
    res_headlines = doc.cssselect('h3.r a')  #get all the <a> tags from <h3 class='r'
    return res_headlines
    
def get_top_google_result(search_query):
    res_headlines = get_google_results(search_query)
    try:
        first_result = res_headlines[0]
    except IndexError:
        print "wtf no search result for %s" %search_query
        return "", ""
    return first_result.text_content(), first_result.get('href')

if __name__ == "__main__":
    main()
