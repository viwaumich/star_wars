import csv
import json
import requests

from urllib.parse import quote, urlencode, urljoin

# Constants
NONE_VALUES = ("", "n/a", "none", "unknown")
CACHE_FILEPATH = "./CACHE.json"


def convert_none_values(data, convert):
    """Attempts to convert certain < data > values to < None > by passing each value in < data >
    along with < convert > to the function < convert_to_none >.

    Loops over the < data > items and calls < convert_to_none > to transform values found in
    < convert > from within a dictionary comprehension. Existing < data > keys are used in the new
    dictionary produced by the comprehension.

    Parameters:
        data (dict): source data
        convert (tuple): strings to convert to None

    Returns:
        dict: new dictionary in which values found in < convert > have been replaced by
              < None >
    """

    return {k: convert_to_none(v, convert) for k, v in data.items()}


def convert_to_float(value):
    """Attempts to convert a string, number, or boolean < value > in the < try > block to a float.
    Can also convert numbers masquerading as strings that include one or more thousand separator
    commas (e.g., "5,000,000").

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (obj): string or number to be converted

    Returns:
        float|any: float if value successfully converted; otherwise returns value unchanged
    """
    try:
        if isinstance(value, str):
            value = value.replace(',', '')

        return float(value)
    except:
        return value


def convert_to_int(value):
    """Attempts to convert a string, number boolean < value > in the < try > block to an integer.
    Can also convert numbers masquerading as strings that include one or more thousand separator
    commas (e.g., "5,000,000") or a period that designates a fractional component
    (e.g., "5,000,000.9999").

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (str|int): string or number to be converted

    Returns:
        int|any: integer if value successfully converted else returns value unchanged
    """
    try:
        value = value.replace(",", "")
        return int(value)
    except:
        return value


def convert_to_list(value, delimiter=None):
    """Attempts to convert a string < value > to a list in the < try > block using the provided
    < delimiter >. Removes leading/trailing spaces before converting < value > to a list.

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (str): string to be split.
        delimiter (str): optional delimiter provided for splitting the string

    Returns:
         list|any: list if value successfully converted else returns value unchanged
    """
    try:
        if delimiter:
            return value.strip().split(delimiter)
        else:
            return value.strip().split()
    except:
        return value

def convert_to_none(value, convert):
    """Attempts to convert the passed in < value > to < None > in the < try > block if the < value >
    matches any of the strings representing null/none values in the passed in tuple < convert >.

    Leading/trailing spaces are removed from the < value > before a case insensitive comparison is
    performed between the < value > and the < convert > items. If a match is obtained < None > is
    returned; otherwise the < value > is returned unchanged.

    If a runtime exception is encountered the < value > is returned unchanged in the except block.

    Parameters:
        value (obj): string or number to be converted
        convert (tuple): strings to convert to None

    Returns:
        None|any: if value successfully converted; otherwise returns value unchanged
    """

    try:
        if value.lower().strip() in convert:
            return None
        else:
            return value
    except:
        return value


def create_cache(filepath):
    """Attempts to retrieve cache contents written to the file system. If successful the
    cache contents from the previous script run are returned to the caller as the new
    cache. If unsuccessful an empty cache is returned to the caller.

    Parameters:
        filepath (str): path to the cache file

    Returns:
        dict: cache either empty or populated with resources from the previous script run
    """

    try:
        return read_json(filepath)
    except FileNotFoundError:
        return {}


def create_cache_key(url, params=None):
    """Returns a lowercase string key comprising the passed in < url >, and, if < params >
    is not None, the "?" separator, and any URL encoded querystring fields and values.
    Passes to the function < urllib.parse.urljoin > the optional < quote_via=quote >
    argument to override the default behavior and encode spaces with '%20' rather
    than "+".

    Example:
       url = https://swapi.py4e.com/api/people/
       params = {'search': 'Anakin Skywalker'}
       returns 'https://swapi.py4e.com/api/people/?search=anakin%20skywalker'

    Parameters:
        url (str): string representing a Uniform Resource Locator (URL)
        params (dict): one or more key-value pairs representing querystring fields and values

    Returns:
        str: Lowercase "key" comprising the URL and accompanying querystring fields and values
    """

    if params:
        return urljoin(url, f"?{urlencode(params, quote_via=quote)}").lower()  # space replaced with '%20'
    else:
        return url.lower()


def get_resource(url, params=None, timeout=10):
    """Returns a response object decoded into a dictionary. If query string < params > are
    provided the response object body is returned in the form on an "envelope" with the data
    payload of one or more entities to be found in ['results'] list; otherwise, response
    object body is returned as a single dictionary representation of the entity.

    Parameters:
        url (str): a uniform resource locator that specifies the resource.
        params (dict): optional dictionary of querystring arguments.
        timeout (int): timeout value in seconds.

    Returns:
        dict: dictionary representation of the decoded JSON.
    """

    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()


def read_csv_to_dicts(filepath, encoding="utf-8", newline="", delimiter=","):
    """Accepts a file path, creates a file object, and returns a list of dictionaries that
    represent the row values using the cvs.DictReader().

    WARN: This function must be implemented using a list comprehension in order to earn points.

    Parameters:
        filepath (str): path to file.
        encoding (str): name of encoding used to decode the file.
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences.
        delimiter (str): delimiter that separates the row values.

    Returns:
        list: nested dictionaries representing the file contents.
    """

    with open(filepath, "r", newline=newline, encoding=encoding) as file_obj:
        # data = []
        # reader = csv.DictReader(file_obj, delimiter=delimiter)
        # for line in reader:
        #     data.append(line) # OrderedDict() | alternative: data.append(dict(line))

        reader = csv.DictReader(file_obj, delimiter=delimiter)
        return [line for line in reader]


def read_json(filepath, encoding="utf-8"):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file.
        encoding (str): name of encoding used to decode the file.

    Returns:
        dict/list: dict or list representations of the decoded JSON document.
    """

    with open(filepath, "r", encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding="utf-8", ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file.
        data (dict)/(list): the data to be encoded as JSON and written to the file.
        encoding (str): name of encoding used to encode the file.
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON.

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
