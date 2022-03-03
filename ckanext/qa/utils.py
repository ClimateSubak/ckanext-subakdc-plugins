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
        
    return extras