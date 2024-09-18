from django.urls import path
from RestfulApi.api.CacheLog import getCache
from RestfulApi.api.Auth import AuthApi, Auth
from RestfulApi.api.Register import RegisterSuperUserView, RegisterView
from RestfulApi.api.UpdateUser import UserUpdateDelete, UserUpdate, UserUpdateById, SuperUserUpdateById
from RestfulApi.api.Server import ServerGet, UpdateDeleteServer
from RestfulApi.api.CacheLog import getCache
from RestfulApi.api.StoreLog import getStore, UpdateAutoStoreLog
from RestfulApi.api.Agent import getAgent
from RestfulApi.api.AccesLog import getAcces, UpdateAutoAccesLog

urlpatterns = [
    path('getcache/', getCache.as_view()),
    path('auth/', Auth.as_view()),
    path('register_superuser/', RegisterSuperUserView.as_view()),
    path('register_user/', RegisterView.as_view()),
    path('update_data_user_all/<str:username>/', UserUpdateDelete.as_view()),
    path('update_data_user/<str:username>/', UserUpdate.as_view()),
    path('update_data_user_id/<int:id>/', UserUpdateById.as_view()),
    path('update_data_super_user_id/<int:id>/', SuperUserUpdateById.as_view()),
    path('servercreate/', ServerGet.as_view()),
    path('serverupdatedelete/<int:id>/', UpdateDeleteServer.as_view()),
    path('cachelogview/', getCache.as_view()),
    path('storelogview/', getStore.as_view()),
    path('agentlogview/', getAgent.as_view()),
    path('acceslogview/', getAcces.as_view()),
    path('acceslogupdate/', UpdateAutoAccesLog.as_view()),
    path('storelogupdate/', UpdateAutoStoreLog.as_view()),
    path('agentlogupdate/', UpdateAutoAccesLog.as_view()), 
]
