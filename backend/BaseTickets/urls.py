from rest_framework import routers
from BaseTickets.api import TiqueViewSet,UsuarioViewSet,ClienteViewSet,UserViewSet,TipoTiqueViewSet,PublicTiqueView,AreaViewSet,EstadoTiqueViewSet,CriticidadViewSet



router = routers.DefaultRouter()

router.register('api/Tiques',TiqueViewSet,'Tiques')
router.register('api/Usuario',UsuarioViewSet,'Usuario')
router.register('api/Cliente',ClienteViewSet,'Cliente')
router.register('api/Cuenta',UserViewSet,'Cuenta')
router.register('api/TipoTique',TipoTiqueViewSet,'TipoTique')
router.register('api/Area',AreaViewSet,'Area')
router.register('api/EstadoTique',EstadoTiqueViewSet,'EstadoTique')
router.register('api/Criticidad',CriticidadViewSet,'Criticidad')


urlpatterns =router.urls