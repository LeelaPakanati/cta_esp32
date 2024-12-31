def prepare_url(url, params):
    return_url = url + "?"
    for (param,value) in params.items():
        return_url += str(param) + "=" 
        if isinstance(value, list):
            for val in value:
                return_url += str(val) + ','
            return_url = return_url[:-1]
            return_url += '&'
        else :
            return_url += str(value) + '&'
    return return_url[:-1]
