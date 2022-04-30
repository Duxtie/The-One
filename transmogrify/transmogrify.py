from datetime import datetime


# For the raw events given (a List of Dictionaries) returns normalized log events as a List of
# Dictionaries having the following keys: 'server', 'date', 'severity', 'process', 'message'.
def transmogrify(raw_events: [dict]) -> [dict]:
    # Write your solution here and in any helper functions you wish to create.
    # Do not change this function signature or this could break tests.

    date_format = '%Y-%m-%dT%H:%M:%S.%f'

    actual_event = []
    for event in raw_events:

        new_event = dict()

        # set date format
        # event['date'] = get_date(date_format, event)

        new_event['server'] = event['server']
        new_event['date'] = get_date(date_format, event['date'])
        new_event['process'] = event.get('process', "")
        new_event['severity'] = event.get('severity', "")
        new_event['message'] = event.get('message', "")

        # set source or return process
        new_event['process'] = event.get('source', event.get('process'))

        if "events" in event:
            for child_event in event['events']:
                new_event['severity'] = get_indicator_level(child_event['indicator-level'])

                if child_event['indicator-type'] == "message":
                    new_event['message'] = child_event['indicator-value']
                else:
                    new_event['message'] = "{type} {value}".format(type=child_event['indicator-type'],
                                                                   value=child_event['indicator-value'])

                actual_event.append(new_event.copy())
        else:
            actual_event.append(new_event)

    return actual_event


def get_date(date_format, value):
    if isinstance(value, int):
        # convert from millisecond to seconds
        if len(str(value)) == 13:
            value = value / 1000

        date = datetime.utcfromtimestamp(value).strftime(date_format)
    else:
        date = datetime.strptime(value, date_format).strftime(date_format)

    return date


def get_indicator_level(value) -> str:
    type_name = None
    if value in range(0, 1):
        type_name = 'TRACE'

    if value == 2:
        type_name = 'DEBUG'

    if value in range(3, 5):
        type_name = 'INFO'

    if value in range(6, 8):
        type_name = 'WARN'

    if value in range(9, 10):
        type_name = 'ERROR'

    return type_name
