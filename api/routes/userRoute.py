from django.urls import path,include
from api.views import userView

urlpatterns = [
    path('signup/',userView.signup,name="signup"),
    
    path('changePassword/',userView.changePassword,name="changePassword"),

    path('api-token-auth/', userView.LoginAuthToken.as_view(),name='api_token_auth'),

    path('info/', userView.UserInfo.as_view(), name='info'),

    path('createSuperUser',userView.createSuperUser,name='create')
]
