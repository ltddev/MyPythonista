import location, speech, time
#from __future__ import print_function  # force print() instead of print

def say_us_english(text):
    speech.say(text, 'en-US', 0.05)
    
def get_city_and_country():
    location.start_updates()
    loc = location.get_location()
    location.stop_updates()
    try:
        addressDict = location.reverse_geocode(loc)[0]  # grab the first loc
        return 'in {City} {Country}'.format(**addressDict)
    except (TypeError, KeyError) as e:
            print('Error in createCurrentLocationString(): {}'.format(e))
    return ''
            
def get_city_country_and_time(in_time=None):
    in_time = in_time or time.localtime()
    loc_time_dict = {
        'location' : get_city_and_country(),
        'hour'     : in_time.tm_hour % 12 or 12,
        'minute'   : 'oh {}'.format(in_time.tm_min) if 0 < in_time.tm_min < 10 else in_time.tm_min,
        'ampm'     : 'A.M.' if in_time.tm_hour < 12 else 'P.M.',
        'second'   : '{} seconds'.format(in_time.tm_sec) }
    if in_time.tm_sec == 0:
        loc_time_dict['second'] = ''
    elif in_time.tm_sec == 1:
        loc_time_dict['second'] = loc_time_dict['second'][:-1]  #strip of the 's'
    fmt = 'The current local time {location} is {hour} {minute} {ampm} {second}.'
    return fmt.format(**loc_time_dict)
        
say_us_english(get_city_country_and_time())
