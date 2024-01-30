from disnake.ext import commands
from datetime import timedelta
import re


def from_str_to_timedelta(str_timedelta: str) -> timedelta:
    """Takes strings like '12m', '3d', '5h', '53s' and returns timedelta."""
    match = re.fullmatch(r'\d{,2}[d,h,m,s]', str_timedelta)
    if match is None:
        raise commands.errors.BadArgument(f'Invalid time was entered: "{str_timedelta}".')

    if 'd' in str_timedelta:
        time = float(str_timedelta.split('d')[0])
        return timedelta(days=time)
    elif 'h' in str_timedelta:
        time = float(str_timedelta.split('h')[0])
        return timedelta(hours=time)
    elif 'm' in str_timedelta:
        time = float(str_timedelta.split('m')[0])
        return timedelta(minutes=time)
    elif 's' in str_timedelta:
        time = float(str_timedelta.split('s')[0])
        return timedelta(seconds=time)
        
