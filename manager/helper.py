
def validate_other_than_already_exists_error(serialized_object):
    # If there are any errors related already exist, then remove these errors.
    # return False, if no errors other than already exists is present in all errors
    if serialized_object.is_valid():
        True
    other_errors = {}
    error_present = False
    for field, errors in serialized_object.errors.items():
        other_errors[field] = [error  for error in errors if "already exists" not in error]
        if len(other_errors[field]) > 0:
            error_present = True
    return error_present if not error_present else other_errors