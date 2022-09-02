from django.urls import path
from .views import *


urlpatterns = [
    path('deleteVoter', deleteVoter, name = "deleteVoter"),
    path('editVoter/<int:id>', editVoter, name = "editVoter"),
    path('votesList', votesList, name = "votesList"),
    path('voterList', voterList, name = "voterList"),
    path('editVoter', editVoter, name = "editVoter"),
    path('deleteVoter', deleteVoter, name = "deleteVoter"),
    path('getVoter', getVoter, name = "getVoter"),
    path('candidatesList', candidatesList, name = "candidatesList"),
    path('positionsList', positionsList, name = "positionsList"),
    path('addCandidate', addCandidate, name = "addCandidate"),
    path('getCandidate', getCandidate, name = "getCandidate"),
    path('editCandidate', editCandidate, name = "editCandidate"),
    path('deleteCandidate', deleteCandidate, name = "deleteCandidate"),

]