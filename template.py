import re

def bind(template, params, pattern='__(.+?)__'):

    def get_param_if_exists(matches):
        original  = str(matches.group(0))
        param_key = str(matches.group(1))
        return params.get(param_key, original)

    if type(template) is str:
        ret = re.sub(pattern, get_param_if_exists, template)
    elif type(template) is dict:
        ret = {}
        for key in template:
            ret[key] = bind(template[key], params, pattern)
    elif type(template) is list:
        ret = []
        for template_item in template:
            ret.append( bind(template_item, params, pattern) )
    else:
        return None

    return ret


if __name__ == '__main__':
	pass
