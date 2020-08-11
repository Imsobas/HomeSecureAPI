from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profle"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class UpdatedOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""


    # Note: The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed.
    
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        ##user_profile = email 
        ##user_profile.id = number eg. 1 
        print(request.user.is_active)

        # {
        # '_request': <WSGIRequest: POST '/api/feed/'>, 
        # 'parsers': [<rest_framework.parsers.JSONParser object at 0x108925f50>, <rest_framework.parsers.FormParser object at 0x108ae4490>, <rest_framework.parsers.MultiPartParser object at 0x108ae4210>], 
        # 'authenticators': [<rest_framework.authentication.TokenAuthentication object at 0x108ae4ad0>], 
        # 'negotiator': <rest_framework.negotiation.DefaultContentNegotiation object at 0x108834990>, 
        # 'parser_context': {'view': <first_api.views.UserProfileFeedViewSet object at 0x1088b3310>, 
        # 'args': (), 
        # kwargs': {}, 
        # 'request': <rest_framework.request.Request object at 0x108ae9fd0>, 
        # 'encoding': 'utf-8'}, 
        # '_data': {'status_text': 'test 2231312'}, 
        # '_files': <MultiValueDict: {}>, 
        # '_full_data': {'status_text': 'test 2231312'}, 
        # '_content_type': <class 'rest_framework.request.Empty'>, 
        # '_stream': <WSGIRequest: POST '/api/feed/'>, 
        # 'method': 'POST', 
        # '_user': <UserProfile: supakorn.silla@gmail.com>, 
        # '_auth': <Token: 79b7236b5a82bc2e62fc21238425733beac60039>, 
        # '_authenticator': <rest_framework.authentication.TokenAuthentication object at 0x108ae4ad0>, 
        # 'accepted_renderer': <rest_framework.renderers.BrowsableAPIRenderer object at 0x108ae4350>, 
        # 'accepted_media_type': 'text/html; q=1.0', 
        # 'version': None, 
        # 'versioning_scheme': None
        # }


        return obj.user_profile.id == request.user.id ## return true, if allow 

