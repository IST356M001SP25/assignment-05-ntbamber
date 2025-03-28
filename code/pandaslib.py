from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''
    cleaned_item = ''.join(char for char in item if char.isdigit() or char == '.')#Extracts all characters that are digits or .
    return float(cleaned_item)    

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    date = datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S')  # parse the full timestamp
    return date.year #return the year

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    possibilities = [
        'united states of america', 'u sa', 'us', 'united states', 'u.s.', 'usa'
    ]
    item_lower = item.lower().strip() #standardizes input to lowercase and removes leading/trailing whitespaces
    if item_lower in possibilities: #checks if item is in possibilities
        return 'United States' #returns 'United States'
    else:
        # Return the original item if no match is found
        return item


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

