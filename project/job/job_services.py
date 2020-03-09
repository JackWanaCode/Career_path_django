from job.models import JobDb, Job


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


def get_job_db_by_id(job_id):
    """get all job seen list"""
    try:
        return JobDb.objects.get(id=job_id)
    except JobDb.DoesNotExist:
        return None

def add_job(job_db_id, user):
    job_db_obj = get_job_db_by_id(job_db_id)
    try:
        new_job_seen = Job(
            company=job_db_obj.company,
            location=job_db_obj.location,
            position=job_db_obj.position,
            description=job_db_obj.description,
            html_description=job_db_obj.html_description,
            link=job_db_obj.link,
            user=user
        )
        print("error 1")
        new_job_seen.save()
        print("error 2")
        return new_job_seen
    except Exception as e:
        print("Error during creating Job object, error is: ", e)
        return None

def get_job_list_by_user_id(user_id):
    try:
        job = Job.objects.filter(user_id=user_id)
        if job != []:
            return job
        else:
            print("job list is empty")
            return None
    except Exception as e:
        print("Error is:", e)
        return None


def get_job_by_id(job_id):
    try:
        return Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return None