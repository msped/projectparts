from .models import Profile

def check_profile(request):
    """Check profile is complete"""
    profile_incomplete = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(id=request.user.id)

        model_check = [
            profile.phone_number,
            profile.address_line_1,
            profile.town_city,
            profile.county,
            profile.country,
            profile.postcode
        ]

        for item in model_check:
            if item == '':
                profile_incomplete = True
                break

    return {
        'profile_incomplete': profile_incomplete
    }
