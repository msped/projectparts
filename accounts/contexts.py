from .models import Profile

def check_profile(request):
    """Check profile is complete"""

    if request.user.is_authenticated:

        profile = Profile.objects.get(id=request.user.id)

        if profile.phone_number == 'Phone No.' and profile.county == "County":
            profile_incomplete = True
        else:
            profile_incomplete = False
    else:
        profile_incomplete = False

    return {
        'profile_incomplete': profile_incomplete
    }
