# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.urls import path, re_path

# from createPaper import views

urlpatterns = [

    # The home page
    path('', index),
    path('insertitem', insertItem),
    path('paperscontestados', paperscontestados),
    path('erroproposta', erroProposta),
    path('insertitempaper', createItem),
    path('listpaperitem', itensPapers),
    path('usepaper', usePaper),
    path('contestar/<int:id>', contestar),
    path('rankingmes', rankingMes),
    path('usepapernaovenda', usePaperNaoVenda),
    path('usepaper/createpaper', createPaper),
    path('gerarelatorio/criarelatorio', geraRelatorioDownload),
    path('selecao/paper', geraSelecao),
    path('gerarelatorivendedor', geraRelatorioVendedor),
    path('gerarelatorio/criarelatoriootimo', geraRelatorioOtimoDownload),
    path('usepapernaovenda/createpaper', createPaperNaoVenda),
    path('paperitens/excluir/<int:id>', excluir_paperIten),
    path('paperitens/editar/<int:id>', editar_item_paper),
    path('paper/editar/<int:id>', editar_paper),
    path('paperitensassociados/editar/<int:id>', editar_item_paper_associado),
    path('paperitensassociados/excluir/<int:id>', excluir_paper_item_associado),
    path('paperitens/editar/paperitens/editar/paperitens/editar_item_salvar/<int:id>', editar_item_salvar),
    path(
        'paperitensassociados/editar/paperitensassociados/editar/paperitensassociados/editar_item_associado_salvar/<int:pk>',
        editar_item_associado_salvar),
    path('contestar/salvarcontestacao/<int:pk>',salvar_contestacao),
    path('paper/editar/paper/editar/paper/editar_paper/<int:id>', editar_paper_salvar),
    path('paper/excluir/<int:id>', excluir_paper),
    path('paperaudio/download/<int:id>', download_gravacao),
    path('paper/view/<int:id>', view_paper),
    path('paper/viewcontest/<int:id>', view_paper_contest),
    path('listpaper', papers),
    path('papersfiltro', listFiltro),
    path('gerarelatorio', geraRelatorio),
    path('listpaperuser', papersUser),
    path('versoes', versoes),
    path('geranovaversao', gera_nova_versao),
    path('visualizaritens/visualiza', visualiza_versoes),
    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),

]
