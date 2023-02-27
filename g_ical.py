import datetime
import re
import dateutil.rrule

_JST = datetime.timezone( datetime.timedelta(hours=+9), 'JST' )

def parse(ical, rrule_look_ahead_days=None):
    is_vevent = False
    tmp_dict = dict()
    ret_list = list()

    for line in ical.splitlines():
        key, value = line.split(':',1)

        if key == 'BEGIN' and value == 'VEVENT':
            is_vevent = True
            continue

        if key == 'END' and value == 'VEVENT':
            is_vevent = False
            ret_list.append(tmp_dict)

            if 'RRULE' in tmp_dict.keys() and 'DTSTART' in tmp_dict.keys() and rrule_look_ahead_days is not None:
                tmp_dict['RRULE'] = dateutil.rrule.rrulestr(s=tmp_dict['RRULE'], dtstart=tmp_dict['DTSTART'])
                event_period = tmp_dict['DTEND'] - tmp_dict['DTSTART']
                before = datetime.datetime.now(_JST) + datetime.timedelta(days=rrule_look_ahead_days)
                expanded_rrule = list( tmp_dict['RRULE'].between(after=tmp_dict['DTSTART'], before=before) )

                for rrule_start_dt in expanded_rrule:
                    tmp_dict = dict(tmp_dict)
                    tmp_dict['DTSTART'] = rrule_start_dt
                    tmp_dict['DTEND'] = rrule_start_dt + event_period
                    ret_list.append(tmp_dict)

            tmp_dict = dict()
            continue

        if not is_vevent:
            continue

        else:
            try:
                value = datetime.datetime.strptime(value.replace('Z', '+0000'), '%Y%m%dT%H%M%S%z').astimezone(_JST)
            except ValueError:
                pass

            try:
                key, value_type = key.split(';')
                if value_type == 'VALUE=DATE':
                    value = datetime.datetime.strptime(value, '%Y%m%d').replace(tzinfo=_JST)
                if value_type == 'TZID=Asia/Tokyo':
                    value = datetime.datetime.strptime(value, '%Y%m%dT%H%M%S').replace(tzinfo=_JST)
            except ValueError:
                pass

        tmp_dict[key] = value

    return ret_list


if __name__ == '__main__':
    pass
