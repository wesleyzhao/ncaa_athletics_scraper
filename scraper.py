import requests
import lxml
from lxml.html import parse
import csv
GOOGLE_URL = "http://www.google.com/search?q="
FILE_PATH = "/home/wesley/Downloads/"
FILE_NAME = "d3schools.csv"
def main():
    rows = get_athletic_sites_from_file(FILE_PATH+FILE_NAME)
    write_athletic_sites_to_file(FILE_PATH+"scraper_result.csv", rows)

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
            writer.writerow([row[0],"",row[2]])
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
