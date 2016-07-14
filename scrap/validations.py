from voluptuous import Schema, ALLOW_EXTRA, Invalid
from django.utils.dateparse import parse_datetime, parse_date


def CSVofIntegers(msg=None):
    '''
    Checks whether a value is list of integers.
    Returns list of integers or just one integer in
    list if there is only one element in given CSV string.
    '''
    def fn(value):
        try:
            if isinstance(value, str):
                if ',' in value:
                    value = map(
                        int, filter(
                            bool, map(
                                lambda x: x.strip(), value.split(',')
                            )
                        )
                    )
                    return value
                else:
                    return [int(value)]
        except ValueError:
            raise Invalid(
                '<{0}> is not a valid csv of integers'.format(value)
            )
    return fn


def IntegerLike(msg=None):
    '''
    Checks whether a value is:
        - int, or
        - long, or
        - float without a fractional part, or
        - str or unicode composed only of digits
    '''
    def fn(value):
        if not (
            isinstance(value, int) or
            (isinstance(value, float) and value.is_integer()) or
            (isinstance(value, str) and value.isdigit()) or
            (isinstance(value, str) and value.isdigit())
        ):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an integer'.format(value))
            )
        else:
            return value
    return fn


def DatetimeWithTZ(msg=None):
    '''
    Checks whether a value is :
        - a valid castable datetime object with timezone.
    '''
    def fn(value):
        try:
            date = parse_datetime(value) or parse_date(value)
            if date is not None:
                return date
            else:
                raise ValueError
        except ValueError:
            raise Invalid('<{0}> is not a valid datetime.'.format(value))
    return fn


base_query_param_schema = Schema(
    {
        'q': str,
        'name': str,
        'offset': IntegerLike(),
        'limit': IntegerLike(),
        'install_ts': DatetimeWithTZ(),
        'update_ts': DatetimeWithTZ()
    },
    extra=ALLOW_EXTRA
)


company_query_schema = base_query_param_schema.extend(
    {
        "id": IntegerLike(),
        "name": str,
        "description": str,
        "auction_id": CSVofIntegers(),  # /?team_id=1,2,3
    }
)
