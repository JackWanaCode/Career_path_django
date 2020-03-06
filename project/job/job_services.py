from job.models import JobDb


def get_job_list(position, location):
    job_list = [job for job in JobDb.objects.all()]
    if location == 'None' and position == 'None':
        sorted_job_list = sorted(job_list, key=lambda k: k.date_post)
    else:
        if location != 'None' and position != 'None':
            location = " ".join(location.split('_'))
            position = " ".join(position.split('_'))
            filter_list = [job for job in job_list if (
                        relative_compare(position, job.position) and relative_compare(location, job.location))]
        elif location == 'None':
            position = " ".join(position.split('_'))
            filter_list = [job for job in job_list if (relative_compare(position, job.position))]
        else:
            location = " ".join(location.split('_'))
            filter_list = [job for job in job_list if (relative_compare(location, job.location))]
        sorted_job_list = sorted(filter_list, key=lambda k: k.date_post)
    return sorted_job_list


def relative_compare(user_info, job_req):
    """Function to compare 2 list, if matching greater than 30% return true"""
    user_list = [item.lower() for item in user_info.replace(',', '').replace(' USA', '').split(' ')]
    job_list = [item.lower() for item in job_req.replace(',', '').replace(' USA', '').split(' ')]
    sub_set = set(user_list).intersection(set(job_list))
    m = len(sub_set) / len(job_list)
    if m >= 0.2:
        return True
    return False
