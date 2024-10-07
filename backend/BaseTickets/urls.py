from rest_framework import routers
from BaseTickets.api import TiqueViewSet,UsuarioViewSet,ClienteViewSet,UserViewSet


router = routers.DefaultRouter()

router.register('api/Tiques',TiqueViewSet,'Tiques')
router.register('api/Usuario',UsuarioViewSet,'Usuario')
router.register('api/Cliente',ClienteViewSet,'Cliente')
router.register('api/Cuenta',UserViewSet,'Cuenta')


urlpatterns =router.urls