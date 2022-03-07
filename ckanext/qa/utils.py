import ckan.plugins.toolkit as tk

def merge_with_extras(extras, new_key, new_value):
    """
    Takes a key and value to append or update the extras dict
    Returns the updated extras dict
    """
    qa_extra = { 'key': new_key, 'value': new_value }
    idx = [i for i, ex in enumerate(extras) if ex['key'] == new_key]
    if len(idx) > 0:
        extras[idx[0]] = qa_extra
    else:
        extras.append(qa_extra)
        
    # Filter out subak_ prefixed extras
    # extras = list(filter(lambda ex: not ex['key'].startswith('subak_'), extras))
    
    return extras

def should_patch_entity(qa, key, value):
    """
    Checks whether key/value exists within given qa dict
    If not, returns True
    """
    return not (key in qa and qa[key] == value)
    
def get_all_pkgs():
    """
    Calls the CKAN API and returns all the packages in the database
    along with the associated resources
    """
    get_packages = tk.get_action('current_package_list_with_resources')
    
    # Query the API using cursor to find all packages
    page = 0
    all_pkgs = []
    while (True):
        pkgs = get_packages({ 'ignore_auth': True, 'user': None }, 
                            { 'limit': 100, 'offset': page*100 })
        if len(pkgs) > 0:
            all_pkgs = all_pkgs + pkgs
            page += 1
        else:
            break
        
    return all_pkgs