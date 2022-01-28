from accounts.models import Profile

def avatar(request):
    if request.user.is_authenticated:
        return {
            "user_avatar": Profile.avatar_url(request.user)
        }
    else:
        return {}