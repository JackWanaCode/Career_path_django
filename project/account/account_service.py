from account.models import Profile


def get_all_profile(user_id=None):
    """get all prifle based on user id"""
    if user_id:
        profile = Profile.objects.filter(user_id=user_id)
        return profile
    else:
        return None

def get_profile_by_id(id=None):
    if id:
        try:
            return Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return None

def create_profile(**kwargs):
    profile = Profile(
        user=kwargs['user'],
        position=kwargs['position'],
        location=kwargs['location'],
        skills=kwargs['skills']
    )
    profile.save()
    return profile