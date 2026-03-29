import re
import six

from datetime import timedelta

# based on: http://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
parse_regex = re.compile(r'((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')


def parse_timedelta(time_str):
    parts = parse_regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in six.iteritems(parts):
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


__all__ = ["parse_timedelta"]
