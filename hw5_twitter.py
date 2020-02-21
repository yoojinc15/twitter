#########################################
##### Name:   Yoojin Choi           #####
##### Uniqname:   yjinchoi          #####
#########################################

TWITTER_API_KEY = "H8NzNwIZnZ9FgFPUpLTTg5AVM"
TWITTER_API_SECRET = "2wfwES1bbmyceNndMipEdnS2Hx0Q4aHZ17gC2bAm4cfEb1lyPC"
TWITTER_ACCESS_TOKEN = "1227976512718028801-RK891fzMCWoRc32mwTIJmfkJaODRhx"
TWITTER_ACCESS_TOKEN_SECRET = "MrkPb6lBw75zYxpBGEI3nYEAYCIsQl4slbVqRWCWLpyPF"


from requests_oauthlib import OAuth1
import json
import requests
import secrets # file that contains your OAuth credentials

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)


def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    # TODO Implement function

    param_strings = []
    connector = '_'
    for k, v in params.items():
        param_strings.append(f'{k}_{v}')
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    # TODO Implement function

    response = requests.get(baseurl, params=params, auth=oauth).json()
    return response


def make_request_with_cache(baseurl, hashtag, count):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    # TODO Implement function

    params = {'q': hashtag, 'count': count}
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!")
        return CACHE_DICT[request_key]
    else:
        print("cache miss!")
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]


def find_most_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#election2020")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    # TODO: Implement function

    hashtags = []
    hashtag_conter = {}
    for v in tweet_data['statuses']:
        if v['text'][:2] != 'dododot':
            for k in v['entities']['hashtags']:
                hashtag = str(k['text']).lower()
                if hashtag != hashtag_to_ignore.replace('#', ''):
                    hashtags.append(hashtag)
                    try:
                        hashtag_conter[hashtag] += 1
                    except KeyError:
                        hashtag_conter[hashtag] = 1
    print(hashtag_conter)
    most_hashtag = ''
    counter = 0
    for k, v in hashtag_conter.items():
        if v > counter:
            most_hashtag = k
            counter = v

    ''' Hint: In case you're confused about the hashtag_to_ignore 
    parameter, we want to ignore the hashtag we queried because it would 
    definitely be the most occurring hashtag, and we're trying to find 
    the most commonly co-occurring hashtag with the one we queried (so 
    we're essentially looking for the second most commonly occurring 
    hashtags).'''

    return '#' + str(most_hashtag)


if __name__ == "__main__":
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    CACHE_DICT = open_cache()

    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    hashtag = "#2020election"
    count = 100

    tweet_data = make_request_with_cache(baseurl, hashtag, count)
    most_common_cooccurring_hashtag = find_most_common_cooccurring_hashtag(tweet_data, hashtag)
    print("The most commonly cooccurring hashtag with {} is {}.".format(hashtag, most_common_cooccurring_hashtag))
