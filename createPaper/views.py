from datetime import date, datetime
import calendar
from django.template import loader
from django import template
import operator
import psycopg2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
#import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
import uuid
from django.forms.models import model_to_dict

class Contestacoes():
    def contestacoes(self):
        itensassociadosmes = PaperItemAssociado.objects.all()
        contestacoes = 0
        paperscontestados = []
        for item in itensassociadosmes:
            if len(item.contestacao) > 0:
                paperscontestados.append(item.paper)
                contestacoes+=1
        return contestacoes



@login_required(login_url="/login/")
def rankingMes(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        data = datetime.now()
        mes = request.POST.get("rankingmes")
        ano = data.year
        anoesc = request.POST.get("rankingmesano")
        vendedoresmes = []
        listamaiores = {}
        listamaioresmes = {}
        usuarios = User.objects.filter(is_active=True)

        # Cálculo de notas de todos os vendedores no mês.
        for item1 in usuarios:
            for nome in item1.groups.all():
                if str(nome) == "Vendedores":
                    listamaiores[item1] = ''
                    if int(mes) + 1 == 13:
                        ano1 = ano + 1
                        mes1 = '01'
                        listapapers = Paper.objects.filter(id_usuario=item1,
                                                           data_monitoria__range=["% s-% s-01" % (anoesc, mes),
                                                                                  "% s-% s-01" % (
                                                                                      ano1, mes1)])

                    else:
                        listapapers = Paper.objects.filter(id_usuario=item1,
                                                           data_monitoria__range=["% s-% s-01" % (anoesc, mes),
                                                                                  "% s-% s-01" % (
                                                                                      anoesc, int(mes) + 1)])



                    nota = 0
                    tamanho = len(listapapers)
                    for item in listapapers:
                        if int(item.data_monitoria.month) == (int(int(mes)+1)):
                            tamanho = len(listapapers)-1
                            continue
                        nota = nota + (item.pontos + item.pontosComportamental + item.pontosGe)
                    try:
                        listamaioresmes[item1] = round(((nota / tamanho) / 300) * 100)

                    except ZeroDivisionError:
                        listamaioresmes[item1] = 0


        listaAcuraceames = sorted(listamaioresmes.items(), key=operator.itemgetter(1))
        listaAcuraceames = listaAcuraceames[::-1]
        for item in listaAcuraceames:
            vendedoresmes.append(item)

        vendedoresmes = list(vendedoresmes)
        for i in range(len(vendedoresmes)):
            vendedoresmes[i] = list(vendedoresmes[i])
            item = str(vendedoresmes[i][0])
            vendedoresmes[i][0] = item

        meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
                 'novembro', 'dezembro']
        mesvendedores = meses[int(mes)-1]
        return render(request, 'rankingmes.html', context={'vendedoresmes': vendedoresmes, 'mesvendedores':mesvendedores, 'contestacoes':contestacoes, 'numeros': range(2020, 2030)})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required(login_url="/login/")
def index(request):
    contestacoes = Contestacoes.contestacoes('')
    data = datetime.now()
    mes = data.month
    ano = data.year
    total = len(Paper.objects.all())
    totalvenda = len(Paper.objects.filter(tipo="Venda"))
    totalnaovenda = len(Paper.objects.filter(tipo="Não venda"))
    vendedores = []
    vendedoresmes = []
    listamaiores = {}
    listamaioresmes = {}
    usuarios = User.objects.filter(is_active=True)

    # Cálculo de notos de todos os vendedores no mês.
    for item1 in usuarios:
        for nome in item1.groups.all():
            if str(nome) == "Vendedores":
                listamaiores[item1] = ''
                if int(mes)+1 == 13:
                    ano1=ano + 1
                    mes1 = '01'
                    listapapers = Paper.objects.filter(id_usuario=item1, data_monitoria__range=["% s-% s-01" % (ano, mes),"% s-% s-01" % (ano1, mes1)])
                else:
                    listapapers = Paper.objects.filter(id_usuario=item1,
                                                       data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                              "% s-% s-01" % (ano, int(mes)+1)])
                nota = 0
                for item in listapapers:
                    nota = nota + (item.pontos + item.pontosComportamental + item.pontosGe)
                try:
                    listamaioresmes[item1] = round(((nota / len(listapapers)) / 300) * 100)
                except ZeroDivisionError:
                    listamaioresmes[item1] = 0

    listaAcuraceames = sorted(listamaioresmes.items(), key=operator.itemgetter(1))
    listaAcuraceames = listaAcuraceames[::-1]
    for item in listaAcuraceames:
        vendedoresmes.append(item)

    vendedoresmes = list(vendedoresmes)
    for i in range(len(vendedoresmes)):
        vendedoresmes[i] = list(vendedoresmes[i])
        item = str(vendedoresmes[i][0])
        vendedoresmes[i][0] = item

    for item1 in usuarios:
        for nome in item1.groups.all():
            if str(nome) == "Vendedores":
                listamaiores[item1] = ''
                listapapers = Paper.objects.filter(id_usuario=item1)
                nota = 0
                for item in listapapers:
                    nota = nota + (item.pontos + item.pontosComportamental + item.pontosGe)
                try:
                    listamaiores[item1] = round(((nota / len(Paper.objects.filter(id_usuario=item1))) / 300) * 100)
                except ZeroDivisionError:
                    listamaiores[item1] = 0

    listaAcuracea = sorted(listamaiores.items(), key=operator.itemgetter(1))
    listaAcuracea = listaAcuracea[::-1]
    for item in listaAcuracea:
        vendedores.append(item)

    data_atual = date.today()
    data = datetime.now()
    mes = data.month
    ano = data.year
    if int(mes) + 1 == 13:
        ano1= ano + 1
        mes1 = '01'
        totalmes = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano1, mes1)]))

        totalmesvenda = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano1, mes1)],
                                 tipo="Venda"))
        totalmesnaovenda = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano1, mes1)],
                                 tipo="Não venda"))
    else:
        totalmes = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano, int(mes)+1)]))

        totalmesvenda = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano, int(mes)+1)],
                                 tipo="Venda"))
        totalmesnaovenda = len(
            Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, mes), "% s-% s-01" % (ano, int(mes)+1)],
                                 tipo="Não venda"))

    try:
        porcentagem = round((totalmes / total) * 100)
    except ZeroDivisionError:
        porcentagem = 0

    try:
        porcentagemvenda = round((totalmesvenda / total) * 100)
    except ZeroDivisionError:
        porcentagemvenda = 0

    try:
        porcentagemnaovenda = round((totalmesnaovenda / total) * 100)
    except ZeroDivisionError:
        porcentagemnaovenda = 0
    todosUser = len(User.objects.filter(is_active=True))
    itensassociados = PaperItemAssociado.objects.all()
    listaId = {}
    conterros = 0
    for item in itensassociados:
        if item.peso > 0:
            conterros += 1
            if item.paperItem.pk in listaId:
                continue
            listaId[item.paperItem.nome] = 0

    for item in itensassociados:
        if item.peso > 0:
            listaId[item.paperItem.nome] = int(listaId[item.paperItem.nome]) + 1
    # Este dicionário mostra os itens onde ocorrem erros.
    listaId = sorted(listaId.items(), key=operator.itemgetter(1))
    listaId = listaId[::-1]

    dia = data.day
    dia6 = ''
    dia5 = ''
    dia4 = ''
    dia3 = ''
    dia2 = ''
    dia1 = ''

    if len(str(dia)) < 2:
        dia = '0' + str(dia)

        dia6 = '0' + str((int(dia) - 6)).replace('-', '')
        dia5 = '0' + str((int(dia) - 5)).replace('-', '')
        dia4 = '0' + str((int(dia) - 4)).replace('-', '')
        dia3 = '0' + str((int(dia) - 3)).replace('-', '')
        dia2 = '0' + str((int(dia) - 2)).replace('-', '')
        dia1 = '0' + str((int(dia) - 1)).replace('-', '')

    elif len(str(dia)) == 2:
        dia6 = str((int(dia) - 6)).replace('-', '')
        dia5 = str((int(dia) - 5)).replace('-', '')
        dia4 = str((int(dia) - 4)).replace('-', '')
        dia3 = str((int(dia) - 3)).replace('-', '')
        dia2 = str((int(dia) - 2)).replace('-', '')
        dia1 = str((int(dia) - 1)).replace('-', '')

    listadiafinaldosmeses = calendar.mdays

    try:
        if dia == '00':
            dia = listadiafinaldosmeses[mes - 1]
            mes = mes - 1
        totaldiasegunda = len(
            Paper.objects.filter(
                data_monitoria__range=["% s-% s-% s" % (ano, mes, dia), "% s-% s-% s" % (ano, mes, dia)]))
        totaldiavendasegunda1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia), "% s-% s-% s" % (ano, mes, dia)], tipo="Venda"))
        totaldiavendasegunda = round((totaldiavendasegunda1 / totaldiasegunda) * 100)
        totaldianaovendasegunda1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia), "% s-% s-% s" % (ano, mes, dia)], tipo="Não venda"))
        totaldianaovendasegunda = round((totaldianaovendasegunda1 / totaldiasegunda) * 100)

    except ZeroDivisionError:
        totaldiavendasegunda1 = 0
        totaldiavendasegunda = 0
        totaldianaovendasegunda1 = 0
        totaldianaovendasegunda = 0

    try:
        if dia1 == '00':
            dia1 = listadiafinaldosmeses[mes - 1]
            if dia1 == 0:
                dia1 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia1 == '010':
            dia1 = '01'

        if dia1 == '011' or dia1 == '012' or dia1 == '013' or dia1 == '014' or dia1 == '015' or dia1 == '016' or dia1 == '017' or dia1 == '018' or dia1 == '020':
            dia1 = dia1[1:3]

        totaldiaterca = len(Paper.objects.filter(data_monitoria__range=["% s-% s-% s" % (ano, mes, dia1), "% s-% s-% s" % (ano, mes, dia1)]))
        totaldiavendaterca1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia1), "% s-% s-% s" % (ano, mes, dia1)], tipo="Venda"))
        totaldiavendaterca = round((totaldiavendaterca1 / totaldiaterca) * 100)
        totaldianaovendaterca1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia1), "% s-% s-% s" % (ano, mes, dia1)],
            tipo="Não venda"))
        totaldianaovendaterca = round((totaldianaovendaterca1 / totaldiaterca) * 100)
    except ZeroDivisionError:
        totaldiavendaterca1 = 0
        totaldiavendaterca = 0
        totaldianaovendaterca1 = 0
        totaldianaovendaterca = 0

    try:
        if dia2 == '00':
            dia2 = listadiafinaldosmeses[mes - 1]
            if dia2 == 0:
                dia2 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia2 == '010':
            dia2 = '01'

        if dia2 == '011' or dia2 == '012' or dia2 == '013' or dia2 == '014' or dia2 == '015' or dia2 == '016' or dia2 == '017' or dia2 == '018' or dia2 == '020':
            dia2 = dia2[1:3]

        totaldiaquarta = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia2), "% s-% s-% s" % (ano, mes, dia2)]))
        totaldiavendaquarta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia2), "% s-% s-% s" % (ano, mes, dia2)], tipo="Venda"))
        totaldiavendaquarta = round((totaldiavendaquarta1 / totaldiaquarta) * 100)
        totaldianaovendaquarta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia2), "% s-% s-% s" % (ano, mes, dia2)],
            tipo="Não venda"))
        totaldianaovendaquarta = round((totaldianaovendaquarta1 / totaldiaquarta) * 100)
    except ZeroDivisionError:
        totaldiavendaquarta1 = 0
        totaldiavendaquarta = 0
        totaldianaovendaquarta1 = 0
        totaldianaovendaquarta = 0

    try:
        if dia3 == '00':
            dia3 = listadiafinaldosmeses[mes - 1]
            if dia3 == 0:
                dia3 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia3 == '010':
            dia3 = '01'

        if dia3 == '011' or dia3 == '012' or dia3 == '013' or dia3 == '014' or dia3 == '015' or dia3 == '016' or dia3 == '017' or dia3 == '018' or dia3 == '020':
            dia3 = dia3[1:3]

        totaldiaquinta = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia3), "% s-% s-% s" % (ano, mes, dia3)]))
        totaldiavendaquinta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia3), "% s-% s-% s" % (ano, mes, dia3)], tipo="Venda"))
        totaldiavendaquinta = round((totaldiavendaquinta1 / totaldiaquinta) * 100)
        totaldianaovendaquinta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia3), "% s-% s-% s" % (ano, mes, dia3)],
            tipo="Não venda"))
        totaldianaovendaquinta = round((totaldianaovendaquinta1 / totaldiaquinta) * 100)
    except ZeroDivisionError:
        totaldiavendaquinta1 = 0
        totaldiavendaquinta = 0
        totaldianaovendaquinta1 = 0
        totaldianaovendaquinta = 0

    try:
        if dia4 == '00':
            dia4 = listadiafinaldosmeses[mes - 1]
            if dia4 == 0:
                dia4 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia4 == '010':
            dia4 = '01'

        if dia4 == '011' or dia4 == '012' or dia4 == '013' or dia4 == '014' or dia4 == '015' or dia4 == '016' or dia4 == '017' or dia4 == '018' or dia4 == '020':
            dia4 = dia4[1:3]

        totaldiasexta = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia4), "% s-% s-% s" % (ano, mes, dia4)]))
        totaldiavendasexta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia4), "% s-% s-% s" % (ano, mes, dia4)], tipo="Venda"))
        totaldiavendasexta = round((totaldiavendasexta1 / totaldiasexta) * 100)
        totaldianaovendasexta1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia4), "% s-% s-% s" % (ano, mes, dia4)],
            tipo="Não venda"))
        totaldianaovendasexta = round((totaldianaovendasexta1 / totaldiasexta) * 100)
    except ZeroDivisionError:
        totaldiavendasexta1 = 0
        totaldiavendasexta = 0
        totaldianaovendasexta1 = 0
        totaldianaovendasexta = 0

    try:
        if dia5 == '00':
            dia5 = listadiafinaldosmeses[mes - 1]
            if dia5 == 0:
                dia5 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia5 == '010':
            dia5 = '01'

        if dia5 == '011' or dia5 == '012' or dia5 == '013' or dia5 == '014' or dia5 == '015' or dia5 == '016' or dia5 == '017' or dia5 == '018' or dia5 == '020':
            dia5 = dia5[1:3]

        totaldiasabado = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia5), "% s-% s-% s" % (ano, mes, dia5)]))
        totaldiavendasabado1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia5), "% s-% s-% s" % (ano, mes, dia5)], tipo="Venda"))
        totaldiavendasabado = round((totaldiavendasabado1 / totaldiasabado) * 100)
        totaldianaovendasabado1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia5), "% s-% s-% s" % (ano, mes, dia5)],
            tipo="Não venda"))
        totaldianaovendasabado = round((totaldianaovendasabado1 / totaldiasabado) * 100)
    except ZeroDivisionError:
        totaldiavendasabado1 = 0
        totaldiavendasabado = 0
        totaldianaovendasabado1 = 0
        totaldianaovendasabado = 0

    try:
        if dia6 == '00':
            dia6 = listadiafinaldosmeses[mes - 1]
            if dia6 == 0:
                dia6 = listadiafinaldosmeses[mes - 2]
            mes = mes - 1
            if mes == 00:
                mes = 12

        if dia6 == '010':
            dia6 = '01'

        if dia6 == '011' or dia6 == '012' or dia6 == '013' or dia6 == '014' or dia6 == '015' or dia6 == '016' or dia6 == '017' or dia6 == '018' or dia6 == '020':
            dia6 = dia6[1:3]

        totaldiadomingo = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia6), "% s-% s-% s" % (ano, mes, dia6)]))
        totaldiavendadomingo1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia6), "% s-% s-% s" % (ano, mes, dia6)], tipo="Venda"))
        totaldiavendadomingo = round((totaldiavendadomingo1 / totaldiadomingo) * 100)
        totaldianaovendadomingo1 = len(Paper.objects.filter(
            data_monitoria__range=["% s-% s-% s" % (ano, mes, dia6), "% s-% s-% s" % (ano, mes, dia6)],
            tipo="Não venda"))
        totaldianaovendadomingo = round((totaldianaovendadomingo1 / totaldiadomingo) * 100)
    except ZeroDivisionError:
        totaldiavendadomingo1 = 0
        totaldiavendadomingo = 0
        totaldianaovendadomingo1 = 0
        totaldianaovendadomingo = 0

    meses = ['janeiro', 'fevereiro', 'mar', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
             'novembro', 'dezembro']
    try:
        mesvendedores = meses[mes]
    except IndexError:
        mesvendedores = meses[11]

    totaldezembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 12), "% s-% s-01" % (ano, 00 + 1)]))
    totalnovembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 11), "% s-% s-01" % (ano, 11 + 1)]))
    totaloutubro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 10), "% s-% s-01" % (ano, 10 + 1)]))
    totalsetembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 9), "% s-% s-01" % (ano, 9 + 1)]))
    totalagosto = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 8), "% s-% s-01" % (ano, 8 + 1)]))
    totaljulho = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 7), "% s-% s-01" % (ano, 7 + 1)]))
    totaljunho = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 6), "% s-% s-01" % (ano, 6 + 1)]))
    totalmaio = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 5), "% s-% s-01" % (ano, 5 + 1)]))
    totalabril = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 4), "% s-% s-01" % (ano, 4 + 1)]))
    totalmarco = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 3), "% s-% s-01" % (ano, 3 + 1)]))
    totalfevereiro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 2), "% s-% s-01" % (ano, 2 + 1)]))
    totaljaneiro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 1), "% s-% s-01" % (ano, 1 + 1)]))

    totaldezembrov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 12), "% s-% s-01" % (ano, 00 + 1)],
                             tipo="Venda"))
    totalnovembrov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 11), "% s-% s-01" % (ano, 11 + 1)],
                             tipo="Venda"))
    totaloutubrov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 10), "% s-% s-01" % (ano, 10 + 1)],
                             tipo="Venda"))
    totalsetembrov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 9), "% s-% s-01" % (ano, 9 + 1)],
                             tipo="Venda"))
    totalagostov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 8), "% s-% s-01" % (ano, 8 + 1)],
                             tipo="Venda"))
    totaljulhov = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 7), "% s-% s-01" % (ano, 7 + 1)],
                                           tipo="Venda"))
    totaljunhov = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 6), "% s-% s-01" % (ano, 6 + 1)],
                                           tipo="Venda"))
    totalmaiov = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 5), "% s-% s-01" % (ano, 5 + 1)],
                                          tipo="Venda"))
    totalabrilv = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 4), "% s-% s-01" % (ano, 4 + 1)],
                                           tipo="Venda"))
    totalmarcov = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 3), "% s-% s-01" % (ano, 3 + 1)],
                                           tipo="Venda"))
    totalfevereirov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 2), "% s-% s-01" % (ano, 2 + 1)],
                             tipo="Venda"))
    totaljaneirov = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 1), "% s-% s-01" % (ano, 1 + 1)],
                             tipo="Venda"))

    totaldezembronv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 12), "% s-% s-01" % (ano, 00 + 1)],
                             tipo="Não venda"))
    totalnovembronv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 11), "% s-% s-01" % (ano, 11 + 1)],
                             tipo="Não venda"))
    totaloutubronv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 10), "% s-% s-01" % (ano, 10 + 1)],
                             tipo="Não venda"))
    totalsetembronv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 9), "% s-% s-01" % (ano, 9 + 1)],
                             tipo="Não venda"))
    totalagostonv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 8), "% s-% s-01" % (ano, 8 + 1)],
                             tipo="Não venda"))
    totaljulhonv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 7), "% s-% s-01" % (ano, 7 + 1)],
                             tipo="Não venda"))
    totaljunhonv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 6), "% s-% s-01" % (ano, 6 + 1)],
                             tipo="Não venda"))
    totalmaionv = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 5), "% s-% s-01" % (ano, 5 + 1)],
                                           tipo="Não venda"))
    totalabrilnv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 4), "% s-% s-01" % (ano, 4 + 1)],
                             tipo="Não venda"))
    totalmarconv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 3), "% s-% s-01" % (ano, 3 + 1)],
                             tipo="Não venda"))
    totalfevereironv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 2), "% s-% s-01" % (ano, 2 + 1)],
                             tipo="Não venda"))
    totaljaneironv = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 1), "% s-% s-01" % (ano, 1 + 1)],
                             tipo="Não venda"))

    itensassociadosmes = PaperItemAssociado.objects.all()

    papersvendedor = len(Paper.objects.filter(id_usuario=request.user.username))
    papersvendedorv = len(Paper.objects.filter(id_usuario=request.user.username, tipo="Venda"))
    papersvendedornv = len(Paper.objects.filter(id_usuario=request.user.username, tipo="Não venda"))
    if int(mes) + 1 == 13:
        ano1 = ano + 1
        mes1 = '01'
        papersvendedormes = len(Paper.objects.filter(id_usuario=request.user.username,
                                                     data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                            "% s-% s-01" % (ano1, mes1)])),
        papersvendedormesv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                      data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                             "% s-% s-01" % (ano1, mes1)],tipo="Venda")),
        papersvendedormesnv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                       data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                              "% s-% s-01" % (ano1,mes1)],tipo="Não venda")),
    else:
        papersvendedormes = len(Paper.objects.filter(id_usuario=request.user.username,
                                                     data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                            "% s-% s-01" % (ano, int(mes) + 1)])),
        papersvendedormesv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                      data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                             "% s-% s-01" % (ano, int(mes) + 1)],tipo="Venda"))


        papersvendedormesnv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                       data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                              "% s-% s-01" % (ano, int(mes) + 1)],
                                                       tipo="Não venda"))

    try:
        return render(request, "index.html",
                      context={'total': total, 'totalvenda': totalvenda, 'totalnaovenda': totalnaovenda,
                               'totalmes': totalmes, 'totalmesvenda': totalmesvenda,
                               'totalmesnaovenda': totalmesnaovenda,
                               'porcentagem': porcentagem, 'porcentagemvenda': porcentagemvenda,
                               'porcentagemnaovenda': porcentagemnaovenda,
                               'vendedor1': vendedores[0][0], 'vendedor1A': vendedores[0][1],
                               'vendedor2': vendedores[1][0],
                               'vendedor2A': vendedores[1][1], 'vendedor3': vendedores[2][0],
                               'vendedor3A': vendedores[2][1], 'vendedor4': vendedores[3][0],
                               'vendedor4A': vendedores[3][1], 'vendedor5': vendedores[4][0],
                               'vendedor5A': vendedores[4][1], 'vendedor6': vendedores[5][0],
                               'vendedor6A': vendedores[5][1], 'users': todosUser, 'mes': meses[int(mes) - 1],
                               'ano': ano,
                               'erro1': listaId[0][0], 'erro1qt': listaId[0][1], 'erro2': listaId[1][0],
                               'erro2qt': listaId[1][1], 'erro3': listaId[2][0], 'erro3qt': listaId[2][1],
                               'conterros': conterros
                          , 'totaljaneiro': totaljaneiro, 'totalfevereiro': totalfevereiro, 'totalmarco': totalmarco,
                               'totalabril': totalabril,
                               'totalmaio': totalmaio, 'totaljunho': totaljunho, 'totaljulho': totaljulho,
                               'totalagosto': totalagosto, 'totalsetembro': totalsetembro,
                               'totaloutubro': totaloutubro, 'totalnovembro': totalnovembro,
                               'totaldezembro': totaldezembro
                          , 'totaljaneirov': totaljaneirov, 'totalfevereirov': totalfevereirov,
                               'totalmarcov': totalmarcov,
                               'totalabrilv': totalabrilv,
                               'totalmaiov': totalmaiov, 'totaljunhov': totaljunhov,
                               'totaljulhov': totaljulhov, 'totalagostov': totalagostov,
                               'totalsetembrov': totalsetembrov,
                               'totaloutubrov': totaloutubrov, 'totalnovembrov': totalnovembrov,
                               'totaldezembrov': totaldezembrov
                          , 'totaljaneironv': totaljaneironv, 'totalfevereironv': totalfevereironv,
                               'totalmarconv': totalmarconv,
                               'totalabrilnv': totalabrilnv,
                               'totalmaionv': totalmaionv, 'totaljunhonv': totaljunhonv,
                               'totaljulhonv': totaljulhonv, 'totalagostonv': totalagostonv,
                               'totalsetembronv': totalsetembronv,
                               'totaloutubronv': totaloutubronv, 'totalnovembronv': totalnovembronv,
                               'totaldezembronv': totaldezembronv, 'papersvendedor': papersvendedor,
                               'papersvendedormes': papersvendedormes, 'papersvendedormesnv': papersvendedormesnv,
                               'papersvendedormesv': papersvendedormesv, 'contestacoes': contestacoes,
                               'papersvendedorv': papersvendedorv, 'papersvendedornv': papersvendedornv,
                               'vendedoresmes': list(vendedoresmes), 'data_atual': data_atual,
                               'mesvendedores': mesvendedores
                          , 'totaldiavendaquarta': totaldiavendaquarta,
                               'totaldianaovendaquarta': totaldianaovendaquarta,
                               'totaldianaovendaquinta': totaldianaovendaquinta,
                               'totaldianaovendasexta': totaldianaovendasexta,
                               'totaldianaovendasabado': totaldianaovendasabado,
                               'totaldianaovendadomingo': totaldianaovendadomingo,
                               'totaldianaovendasegunda': totaldianaovendasegunda,
                               'totaldianaovendaterca': totaldianaovendaterca,
                               'totaldiavendaterca': totaldiavendaterca,
                               'totaldiavendaquinta': totaldiavendaquinta, 'totaldiavendasexta': totaldiavendasexta,
                               'totaldiavendasabado': totaldiavendasabado,
                               'totaldiavendadomingo': totaldiavendadomingo,
                               'totaldiavendasegunda': totaldiavendasegunda,
                               'totaldiavendaquarta1': totaldiavendaquarta1,
                               'totaldianaovendaquarta1': totaldianaovendaquarta1,
                               'totaldiavendaquinta1': totaldiavendaquinta1,
                               'totaldianaovendaquinta1': totaldianaovendaquinta1,
                               'totaldiavendasexta1': totaldiavendasexta1,
                               'totaldianaovendasexta1': totaldianaovendasexta1,
                               'totaldiavendasabado1': totaldiavendasabado1,
                               'totaldianaovendasabado1': totaldianaovendasabado1,
                               'totaldiavendadomingo1': totaldiavendadomingo1,
                               'totaldianaovendadomingo1': totaldianaovendadomingo1,
                               'totaldiavendasegunda1': totaldiavendasegunda1,
                               'totaldianaovendasegunda1': totaldianaovendasegunda1,
                               'totaldiavendaterca1': totaldiavendaterca1,
                               'totaldianaovendaterca1': totaldianaovendaterca1
                               })

    except IndexError:
        try:
            listaId[0]
        except IndexError:
            listaId = [[0, 0], [0, 0], [0, 0]]
            return render(request, "index.html",
                          context={'total': total, 'totalvenda': totalvenda, 'totalnaovenda': totalnaovenda,
                                   'totalmes': totalmes, 'totalmesvenda': totalmesvenda,
                                   'totalmesnaovenda': totalmesnaovenda,
                                   'porcentagem': porcentagem, 'porcentagemvenda': porcentagemvenda,
                                   'porcentagemnaovenda': porcentagemnaovenda,
                                   'vendedor1': vendedores[0][0], 'vendedor1A': vendedores[0][1],
                                   'vendedor2': vendedores[1][0],
                                   'vendedor2A': vendedores[1][1], 'vendedor3': vendedores[2][0],
                                   'vendedor3A': vendedores[2][1], 'vendedor4': vendedores[3][0],
                                   'vendedor4A': vendedores[3][1], 'vendedor5': vendedores[4][0],
                                   'vendedor5A': vendedores[4][1], 'vendedor6': vendedores[5][0],
                                   'vendedor6A': vendedores[5][1], 'users': todosUser, 'mes': meses[int(mes) - 1],
                                   'ano': ano,
                                   'erro1': listaId[0][0], 'erro1qt': listaId[0][1], 'erro2': listaId[1][0],
                                   'erro2qt': listaId[1][1], 'erro3': listaId[2][0], 'erro3qt': listaId[2][1],
                                   'conterros': conterros
                              , 'totaljaneiro': totaljaneiro, 'totalfevereiro': totalfevereiro,
                                   'totalmarco': totalmarco,
                                   'totalabril': totalabril,
                                   'totalmaio': totalmaio, 'totaljunho': totaljunho, 'totaljulho': totaljulho,
                                   'totalagosto': totalagosto, 'totalsetembro': totalsetembro,
                                   'totaloutubro': totaloutubro, 'totalnovembro': totalnovembro,
                                   'totaldezembro': totaldezembro
                              , 'totaljaneirov': totaljaneirov, 'totalfevereirov': totalfevereirov,
                                   'totalmarcov': totalmarcov,
                                   'totalabrilv': totalabrilv,
                                   'totalmaiov': totalmaiov, 'totaljunhov': totaljunhov,
                                   'totaljulhov': totaljulhov, 'totalagostov': totalagostov,
                                   'totalsetembrov': totalsetembrov,
                                   'totaloutubrov': totaloutubrov, 'totalnovembrov': totalnovembrov,
                                   'totaldezembrov': totaldezembrov
                              , 'totaljaneironv': totaljaneironv, 'totalfevereironv': totalfevereironv,
                                   'totalmarconv': totalmarconv,
                                   'totalabrilnv': totalabrilnv,
                                   'totalmaionv': totalmaionv, 'totaljunhonv': totaljunhonv,
                                   'totaljulhonv': totaljulhonv, 'totalagostonv': totalagostonv,
                                   'totalsetembronv': totalsetembronv,
                                   'totaloutubronv': totaloutubronv, 'totalnovembronv': totalnovembronv,
                                   'totaldezembronv': totaldezembronv, 'papersvendedor': papersvendedor,
                                   'papersvendedormes': papersvendedormes, 'papersvendedormesnv': papersvendedormesnv,
                                   'papersvendedormesv': papersvendedormesv, 'contestacoes': contestacoes,
                                   'papersvendedorv': papersvendedorv, 'papersvendedornv': papersvendedornv,
                                   'vendedoresmes': list(vendedoresmes), 'data_atual': data_atual,
                                   'mesvendedores': mesvendedores
                              , 'totaldiavendaquarta': totaldiavendaquarta,
                                   'totaldianaovendaquarta': totaldianaovendaquarta,
                                   'totaldianaovendaquinta': totaldianaovendaquinta,
                                   'totaldianaovendasexta': totaldianaovendasexta,
                                   'totaldianaovendasabado': totaldianaovendasabado,
                                   'totaldianaovendadomingo': totaldianaovendadomingo,
                                   'totaldianaovendasegunda': totaldianaovendasegunda,
                                   'totaldianaovendaterca': totaldianaovendaterca,
                                   'totaldiavendaterca': totaldiavendaterca,
                                   'totaldiavendaquinta': totaldiavendaquinta, 'totaldiavendasexta': totaldiavendasexta,
                                   'totaldiavendasabado': totaldiavendasabado,
                                   'totaldiavendadomingo': totaldiavendadomingo,
                                   'totaldiavendasegunda': totaldiavendasegunda,
                                   'totaldiavendaquarta1': totaldiavendaquarta1,
                                   'totaldianaovendaquarta1': totaldianaovendaquarta1,
                                   'totaldiavendaquinta1': totaldiavendaquinta1,
                                   'totaldianaovendaquinta1': totaldianaovendaquinta1,
                                   'totaldiavendasexta1': totaldiavendasexta1,
                                   'totaldianaovendasexta1': totaldianaovendasexta1,
                                   'totaldiavendasabado1': totaldiavendasabado1,
                                   'totaldianaovendasabado1': totaldianaovendasabado1,
                                   'totaldiavendadomingo1': totaldiavendadomingo1,
                                   'totaldianaovendadomingo1': totaldianaovendadomingo1,
                                   'totaldiavendasegunda1': totaldiavendasegunda1,
                                   'totaldianaovendasegunda1': totaldianaovendasegunda1,
                                   'totaldiavendaterca1': totaldiavendaterca1,
                                   'totaldianaovendaterca1': totaldianaovendaterca1
                                   })


@login_required(login_url="/login/")
def pages(request):
    contestacoes = Contestacoes.contestacoes('')
    data = datetime.now()
    mes = data.month
    ano = data.year
    totaldezembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 12), "% s-% s-01" % (ano, 00 + 1)],
                             tipo="Venda"))
    totalnovembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 11), "% s-% s-01" % (ano, 11 + 1)],
                             tipo="Venda"))
    totaloutubro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 10), "% s-% s-01" % (ano, 10 + 1)],
                             tipo="Venda"))
    totalsetembro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 9), "% s-% s-01" % (ano, 9 + 1)],
                             tipo="Venda"))
    totalagosto = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 8), "% s-% s-01" % (ano, 8 + 1)],
                                           tipo="Venda"))
    totaljulho = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 7), "% s-% s-01" % (ano, 7 + 1)],
                                          tipo="Venda"))
    totaljunho = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 6), "% s-% s-01" % (ano, 6 + 1)],
                                          tipo="Venda"))
    totalmaio = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 5), "% s-% s-01" % (ano, 5 + 1)],
                                         tipo="Venda"))
    totalabril = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 4), "% s-% s-01" % (ano, 4 + 1)],
                                          tipo="Venda"))
    totalmarco = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 3), "% s-% s-01" % (ano, 3 + 1)],
                                          tipo="Venda"))
    totalfevereiro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 2), "% s-% s-01" % (ano, 2 + 1)],
                             tipo="Venda"))
    totaljaneiro = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 1), "% s-% s-01" % (ano, 1 + 1)],
                             tipo="Venda"))

    totaldezembron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 12), "% s-% s-01" % (ano, 00 + 1)],
                             tipo="Não venda"))
    totalnovembron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 11), "% s-% s-01" % (ano, 11 + 1)],
                             tipo="Não venda"))
    totaloutubron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 10), "% s-% s-01" % (ano, 10 + 1)],
                             tipo="Não venda"))
    totalsetembron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 9), "% s-% s-01" % (ano, 9 + 1)],
                             tipo="Não venda"))
    totalagoston = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 8), "% s-% s-01" % (ano, 8 + 1)],
                             tipo="Não venda"))
    totaljulhon = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 7), "% s-% s-01" % (ano, 7 + 1)],
                                           tipo="Não venda"))
    totaljunhon = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 6), "% s-% s-01" % (ano, 6 + 1)],
                                           tipo="Não venda"))
    totalmaion = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 5), "% s-% s-01" % (ano, 5 + 1)],
                                          tipo="Não venda"))
    totalabriln = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 4), "% s-% s-01" % (ano, 4 + 1)],
                                           tipo="Não venda"))
    totalmarcon = len(Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 3), "% s-% s-01" % (ano, 3 + 1)],
                                           tipo="Não venda"))
    totalfevereiron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 2), "% s-% s-01" % (ano, 2 + 1)],
                             tipo="Não venda"))
    totaljaneiron = len(
        Paper.objects.filter(data_monitoria__range=["% s-% s-01" % (ano, 1), "% s-% s-01" % (ano, 1 + 1)],
                             tipo="Não venda"))

    papersvendedor = len(Paper.objects.filter(id_usuario=request.user.username))
    papersvendedorv = len(Paper.objects.filter(id_usuario=request.user.username, tipo="Venda"))
    papersvendedornv = len(Paper.objects.filter(id_usuario=request.user.username, tipo="Não venda"))

    if int(mes) + 1 == 13:
        mes1 = '01'
        ano1 = ano +1
        papersvendedormes = len(Paper.objects.filter(id_usuario=request.user.username,
                                                     data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                            "% s-% s-01" % (ano1, mes1)]))
        papersvendedormesv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                      data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                             "% s-% s-01" % (ano1, mes1)],
                                                      tipo="Venda"))
        papersvendedormesnv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                       data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                              "% s-% s-01" % (ano1, mes1)],
                                                       tipo="Não venda"))

    else:

        papersvendedormes = len(Paper.objects.filter(id_usuario=request.user.username,
                                                     data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                            "% s-% s-01" % (ano, int(mes) + 1)]))
        papersvendedormesv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                      data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                             "% s-% s-01" % (ano, int(mes) + 1)],
                                                      tipo="Venda"))
        papersvendedormesnv = len(Paper.objects.filter(id_usuario=request.user.username,
                                                       data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                              "% s-% s-01" % (ano, int(mes) + 1)],
                                                       tipo="Não venda"))

    total = len(Paper.objects.all())
    totalvenda = len(Paper.objects.filter(tipo="Venda"))
    totalnaovenda = len(Paper.objects.filter(tipo="Não venda"))

    listapapers = Paper.objects.filter(id_usuario=request.user)
    nota = 0
    for item in listapapers:
        nota = nota + (item.pontos + item.pontosComportamental + item.pontosGe)
    try:
        notalogado = round(((nota / len(Paper.objects.filter(id_usuario=request.user))) / 300) * 100)
    except ZeroDivisionError:
        notalogado = 0

    if int(mes)+1 == 13:
        mes1 = '01'
        ano1 = ano + 1
        listapapersmes = Paper.objects.filter(id_usuario=request.user, data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                                              "% s-% s-01" % (
                                                                                                  ano1, mes1)])
    else:
        listapapersmes = Paper.objects.filter(id_usuario=request.user, data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                                          "% s-% s-01" % (
                                                                                              ano, int(mes) + 1)])
    nota = 0
    for item in listapapersmes:
        nota = nota + (item.pontos + item.pontosComportamental + item.pontosGe)
    try:
        if int(mes) + 1 == 13:
            mes1 = '01'
            ano1 = ano + 1
            notalogadomes = round(((nota / len(Paper.objects.filter(id_usuario=request.user,
                                                                    data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                                           "% s-% s-01" % (ano1, mes1)]))) / 300) * 100)
        else:
            notalogadomes = round(((nota / len(Paper.objects.filter(id_usuario=request.user,
                                                                    data_monitoria__range=["% s-% s-01" % (ano, mes),
                                                                                           "% s-% s-01" % (ano, int(
                                                                                               mes) + 1)]))) / 300) * 100)
    except ZeroDivisionError:
        notalogadomes = 0

    itensassociados = PaperItemAssociado.objects.all()
    itensassociados1 = []

    for item in itensassociados:
        if item.paper.id_usuario == request.user.username:
            itensassociados1.append(item)
        else:
            continue

    listaId = {}
    conterros = 0
    for item in itensassociados1:
        if item.peso > 0:
            conterros += 1
            if item.paperItem.pk in listaId:
                continue
            listaId[item.paperItem.nome] = 0

    for item in itensassociados1:
        if item.peso > 0:
            listaId[item.paperItem.nome] = int(listaId[item.paperItem.nome]) + 1

    # Este dicionário mostra os itens onde ocorrem erros.
    listaId = sorted(listaId.items(), key=operator.itemgetter(1))
    listaId = listaId[::-1]

    itensassociadosmes = PaperItemAssociado.objects.all()
    itensassociadosmes1 = []

    listaId1 = {}
    conterros1 = 0
    for item in itensassociadosmes1:
        if item.peso > 0:
            conterros1 += 1
            if item.paperItem.pk in listaId1:
                continue
            listaId1[item.paperItem.nome] = 0

    for item in itensassociadosmes1:
        if item.peso > 0:
            listaId1[item.paperItem.nome] = int(listaId1[item.paperItem.nome]) + 1

    # Este dicionário mostra os itens onde ocorrem erros.
    listaId1 = sorted(listaId1.items(), key=operator.itemgetter(1))
    listaId1 = listaId1[::-1]


    try:
        context = {'total': total, 'totalvenda': totalvenda, 'totalnaovenda': totalnaovenda,
                   'totaljaneiro': totaljaneiro, 'totalfevereiro': totalfevereiro, 'totalmarco': totalmarco,
                   'totalabril': totalabril, 'totalmaio': totalmaio, 'totaljunho': totaljunho, 'totaljulho': totaljulho,
                   'totalagosto': totalagosto, 'totalsetembro': totalsetembro, 'totaloutubro': totaloutubro,
                   'totalnovembro': totalnovembro, 'totaldezembro': totaldezembro, 'totaljaneiron': totaljaneiron,
                   'totalfevereiron': totalfevereiron, 'totalmarcon': totalmarcon, 'totalabriln': totalabriln,
                   'totalmaion': totalmaion, 'totaljunhon': totaljunhon, 'totaljulhon': totaljulhon,
                   'totalagoston': totalagoston, 'totalsetembron': totalsetembron, 'totaloutubron': totaloutubron,
                   'totalnovembron': totalnovembron, 'totaldezembron': totaldezembron, 'papersvendedor': papersvendedor,
                   'papersvendedorv': papersvendedorv, 'papersvendedornv': papersvendedornv,'contestacoes':contestacoes,
                   'papersvendedormes': papersvendedormes, 'papersvendedormesnv': papersvendedormesnv,
                   'papersvendedormesv': papersvendedormesv, 'notalogado': notalogado, 'notalogadomes': notalogadomes
            , 'erro1': listaId[0][0], 'erro1qt': listaId[0][1], 'erro2': listaId[1][0], 'erro2qt': listaId[1][1],
                   'erro3': listaId[2][0], 'erro3qt': listaId[2][1]
            , 'errom1': listaId1[0][0], 'errom1qt': listaId1[0][1], 'errom2': listaId1[1][0],
                   'errom2qt': listaId1[1][1], 'errom3': listaId1[2][0], 'errom3qt': listaId1[2][1]}
    except IndexError:
        context = {'total': total, 'totalvenda': totalvenda, 'totalnaovenda': totalnaovenda,
                   'totaljaneiro': totaljaneiro, 'totalfevereiro': totalfevereiro, 'totalmarco': totalmarco,
                   'totalabril': totalabril, 'totalmaio': totalmaio, 'totaljunho': totaljunho, 'totaljulho': totaljulho,
                   'totalagosto': totalagosto, 'totalsetembro': totalsetembro, 'totaloutubro': totaloutubro,
                   'totalnovembro': totalnovembro, 'totaldezembro': totaldezembro, 'totaljaneiron': totaljaneiron,
                   'totalfevereiron': totalfevereiron, 'totalmarcon': totalmarcon, 'totalabriln': totalabriln,
                   'totalmaion': totalmaion, 'totaljunhon': totaljunhon, 'totaljulhon': totaljulhon,
                   'totalagoston': totalagoston, 'totalsetembron': totalsetembron, 'totaloutubron': totaloutubron,
                   'totalnovembron': totalnovembron, 'totaldezembron': totaldezembron, 'papersvendedor': papersvendedor,
                   'papersvendedorv': papersvendedorv, 'papersvendedornv': papersvendedornv,'contestacoes':contestacoes,
                   'papersvendedormes': papersvendedormes, 'papersvendedormesnv': papersvendedormesnv ,
                   'papersvendedormesv': papersvendedormesv, 'notalogado': notalogado, 'notalogadomes': notalogadomes}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required
def createItem(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        tipos = ["Não venda", "Venda"]
        versoes = VersaoPaper.objects.all()
        return render(request, 'createItem.html', context={'tipos': tipos, 'versoes': versoes, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def versoes(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        versoes = VersaoPaper.objects.all()
        return render(request, 'versoes.html', context={'versoes': versoes, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def erroProposta(request):
    contestacoes = Contestacoes.contestacoes('')
    return render(request, 'erroproposta.html', context= {'contestacoes':contestacoes})


@login_required
def insertItem(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        tipo = request.POST.get("tipo")
        listaTipo = tipo.split()
        listaTipo = " ".join(listaTipo)
        grupo = request.POST.get("grupo")
        cod = request.POST.get("cod")
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        peso = request.POST.get("peso")
        versao = request.POST.get("versao")
        obj = VersaoPaper.objects.get(versao=versao)

        if nome:
            itemPaper = PaperItem()
            itemPaper.tipo = listaTipo
            itemPaper.grupo = grupo
            itemPaper.cod = cod
            itemPaper.nome = nome
            itemPaper.descricao = descricao
            itemPaper.peso = peso
            itemPaper.versao = obj
            itemPaper.save()

            return redirect('/insertitempaper')
        return redirect('/insertitempaper')
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def itensPapers(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        versao = VersaoPaper.objects.filter().last()

        lista_itens = PaperItem.objects.filter(tipo="Não venda", versao_id=versao)
        lista_itens_proceso = lista_itens.filter(grupo="Processo").order_by('cod')
        lista_itens_tecnica = lista_itens.filter(grupo="Tecnica de venda").order_by('cod')
        lista_itens_comportamental = lista_itens.filter(grupo="Comportamental").order_by('cod')
        lista_itensErro = lista_itens.filter(grupo="Erro grave").order_by('cod')

        lista_itens_venda = PaperItem.objects.filter(tipo="Venda", versao_id=versao)
        lista_itens_proceso_venda = lista_itens_venda.filter(grupo="Processo").order_by('id')
        lista_itens_tecnica_venda = lista_itens_venda.filter(grupo="Tecnica de venda").order_by('cod')
        lista_itens_comportamental_venda = lista_itens_venda.filter(grupo="Comportamental").order_by('cod')
        lista_itensErro_venda = lista_itens_venda.filter(grupo="Erro grave").order_by('cod')
        lista_itens_ge = lista_itens_venda.filter(grupo="Itens ge").order_by('cod')

        return render(request, 'listPaperItens.html',
                      context={'lista_itens_proceso': lista_itens_proceso, 'lista_itens_tecnica': lista_itens_tecnica,
                               'lista_itens_comportamental': lista_itens_comportamental,
                               'lista_itensErro': lista_itensErro,
                               'lista_itens_proceso_venda': lista_itens_proceso_venda,
                               'lista_itens_tecnica_venda': lista_itens_tecnica_venda,
                               'lista_itens_comportamental_venda': lista_itens_comportamental_venda,
                               'lista_itensErro_venda': lista_itensErro_venda, 'lista_itens_ge': lista_itens_ge, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def visualiza_versoes(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        versao = request.POST.get("versao")
        versao = VersaoPaper.objects.get(versao=versao)
        lista_itens = PaperItem.objects.filter(tipo="Não venda", versao_id=versao)
        lista_itens_proceso = lista_itens.filter(grupo="Processo", versao_id=versao).order_by('cod')
        lista_itens_tecnica = lista_itens.filter(grupo="Tecnica de venda", versao_id=versao).order_by('cod')
        lista_itens_comportamental = lista_itens.filter(grupo="Comportamental", versao_id=versao).order_by('cod')
        lista_itensErro = lista_itens.filter(grupo="Erro grave", versao_id=versao).order_by('cod')

        lista_itens_venda = PaperItem.objects.filter(tipo="Venda", versao_id=versao)
        lista_itens_proceso_venda = lista_itens_venda.filter(grupo="Processo", versao_id=versao).order_by('id')
        lista_itens_tecnica_venda = lista_itens_venda.filter(grupo="Tecnica de venda", versao_id=versao).order_by('cod')
        lista_itens_comportamental_venda = lista_itens_venda.filter(grupo="Comportamental", versao_id=versao).order_by(
            'cod')
        lista_itensErro_venda = lista_itens_venda.filter(grupo="Erro grave", versao_id=versao).order_by('cod')
        lista_itens_ge = lista_itens_venda.filter(grupo="Itens ge", versao_id=versao).order_by('cod')

        return render(request, 'listPaperItens.html',
                      context={'lista_itens_proceso': lista_itens_proceso, 'lista_itens_tecnica': lista_itens_tecnica,
                               'lista_itens_comportamental': lista_itens_comportamental,
                               'lista_itensErro': lista_itensErro,
                               'lista_itens_proceso_venda': lista_itens_proceso_venda,
                               'lista_itens_tecnica_venda': lista_itens_tecnica_venda,
                               'lista_itens_comportamental_venda': lista_itens_comportamental_venda,
                               'lista_itensErro_venda': lista_itensErro_venda, 'lista_itens_ge': lista_itens_ge, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def papers(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        papers = Paper.objects.all().order_by('data_monitoria').reverse()
        papersItens = PaperItemAssociado.objects.all()
        return render(request, 'listPaper.html', context={'papers': papers, 'associados': papersItens, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def paperscontestados(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        itensassociadosmes = PaperItemAssociado.objects.all()
        papers = []
        for item in itensassociadosmes:
            if len(item.contestacao) > 0:
                papers.append(item.paper)
        papersItens = PaperItemAssociado.objects.all()

        return render(request, 'listPaperContest.html', context={'papers': papers, 'associados': papersItens, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def papersUser(request):
    contestacoes = Contestacoes.contestacoes('')
    papers = Paper.objects.filter(id_usuario=request.user.username)
    papersAll = Paper.objects.all()
    papersItens = PaperItemAssociado.objects.all()
    usuario = request.user
    for login in usuario.groups.all():
        if str(login) == "Sky":
            return render(request, 'listPaperSky.html', context={'papers': papersAll, 'associados': papersItens, 'contestacoes':contestacoes})
    hora = datetime.now()
    if hora.hour >= 20 and hora.hour < 22:
        return render(request, 'listPaperUser.html', context={'papers': papers, 'associados': papersItens, 'contestacoes':contestacoes})

    elif hora.hour >= 15 and hora.hour < 17:
        return render(request, 'listPaperUser.html',
                      context={'papers': papers, 'associados': papersItens, 'contestacoes': contestacoes})

    else:
        return render(request, 'erroAcesssoHorario.html', context= {'contestacoes':contestacoes})




def usePaper(request):
    contestacoes = Contestacoes.contestacoes('')
    versao = VersaoPaper.objects.filter().last()
    if request.user.is_superuser:
        listaLogins = []
        logins = User.objects.filter(groups__name='Vendedores', is_active=True)
        for item in logins:
            listaLogins.append(item.username)
        lista_itens = PaperItem.objects.filter(tipo="Venda", versao=str(versao.id))
        lista_itens_proceso = lista_itens.filter(grupo="Processo", versao=str(versao.id)).order_by('cod')
        lista_itens_tecnica = lista_itens.filter(grupo="Tecnica de venda", versao=str(versao.id)).order_by('cod')
        lista_itens_comportamental = lista_itens.filter(grupo="Comportamental", versao=str(versao.id)).order_by('cod')
        lista_itensErro = lista_itens.filter(grupo="Erro grave", versao=str(versao.id)).order_by('cod')
        lista_itens_ge = lista_itens.filter(grupo="Itens ge", versao=str(versao.id)).order_by('cod')
        return render(request, 'geraPaper.html',
                      context={'itens': lista_itens, 'itensErro': lista_itensErro, 'processos': lista_itens_proceso,
                               "tecnicas": lista_itens_tecnica, "comportamental": lista_itens_comportamental,
                               "listaLogins": listaLogins, "lista_itens_ge": lista_itens_ge, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def createPaper(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        listaItens = request.POST.getlist("itens")
        lista3 = []
        listaObs1 = request.POST.getlist("obs")
        listaObs = list(filter(None, (listaObs1)))

        if len(listaObs) != len(listaItens):
            return render(request, 'erroItensPendentes.html', context={'listaObs': listaObs, 'listaItens': listaItens, 'contestacoes':contestacoes})

        for i in range(len(listaItens)):
            try:
                listaObs[i]
            except IndexError:
                listaObs.insert(i, "")

        for i in range(len(listaItens)):
            lista2 = [listaItens[i], listaObs[i]]
            lista3.append(lista2)

        tipo = "Venda"
        idUser = request.POST.get("idUser")
        data = request.POST.get("dataMonitoria")
        data_ligacao = request.POST.get("data_ligacao")
        telefone = request.POST.get("telefone")
        proposta = request.POST.get("proposta")
        propostas = Paper.objects.all()
        for item in propostas:
            if item.proposta == proposta:
                return redirect('/erroproposta')
        audio = request.FILES["audio"]
        usuario = request.user.username

        if tipo:
            paper = Paper()
            paper.tipo = tipo
            paper.id_usuario = idUser
            paper.data_monitoria = data
            paper.telefone = telefone
            paper.proposta = proposta
            paper.data_ligacao = data_ligacao
            paper.audio = audio
            paper.usuario = usuario
            paper.save()
            qterrosgraves = 0
            pontos = paper.pontos
            pontosComportamental = paper.pontosComportamental
            pontosGe = paper.pontosGe
            versao = VersaoPaper.objects.filter().last()
            listaTodos = PaperItem.objects.filter(tipo="Venda", versao_id=versao)
            cont = 0
            for item_obj in listaTodos:
                cont += 1
                if item_obj:
                    if item_obj.tipo == "Venda" and str(
                            item_obj.pk) in listaItens and item_obj.grupo == "Itens ge":
                        var = 0
                        for i in range(len(lista3)):
                            if str(lista3[i][0]) == str(item_obj.pk):
                                var = lista3[i][1]
                        relacionamento = PaperItemAssociado()
                        relacionamento.paper = paper
                        relacionamento.paperItem = item_obj
                        relacionamento.peso = item_obj.peso
                        relacionamento.obs = var
                        pontosGe = pontosGe - item_obj.peso
                        relacionamento.save()
                    if item_obj.tipo == "Venda" and str(
                            item_obj.pk) not in listaItens and item_obj.grupo == "Itens ge":
                        relacionamento = PaperItemAssociado()
                        relacionamento.paper = paper
                        relacionamento.paperItem = item_obj
                        relacionamento.peso = 0
                        relacionamento.save()

                    if item_obj.tipo == "Venda" and str(
                            item_obj.pk) not in listaItens and item_obj.grupo != "Comportamental" and item_obj.grupo != "Erro grave" and item_obj.grupo != "Itens ge":
                        relacionamento = PaperItemAssociado()
                        relacionamento.paper = paper
                        relacionamento.paperItem = item_obj
                        relacionamento.peso = 0
                        relacionamento.save()

                    else:
                        if item_obj.tipo == "Venda" and str(
                                item_obj.pk) in listaItens and item_obj.grupo != "Comportamental" and item_obj.grupo != "Erro grave" and item_obj.grupo != "Itens ge":
                            var = 0
                            for i in range(len(lista3)):
                                if str(lista3[i][0]) == str(item_obj.pk):
                                    var = lista3[i][1]
                            relacionamento = PaperItemAssociado()
                            relacionamento.paper = paper
                            relacionamento.paperItem = item_obj
                            relacionamento.peso = item_obj.peso
                            relacionamento.obs = var
                            pontos = pontos - item_obj.peso
                            relacionamento.save()
                        else:
                            if item_obj.tipo == "Venda" and str(
                                    item_obj.pk) not in listaItens and item_obj.grupo == "Comportamental" and item_obj.grupo != "Itens ge":
                                relacionamento = PaperItemAssociado()
                                relacionamento.paper = paper
                                relacionamento.paperItem = item_obj
                                relacionamento.peso = 0
                                relacionamento.save()
                            else:
                                if item_obj.tipo == "Venda" and str(
                                        item_obj.pk) in listaItens and item_obj.grupo == "Comportamental" and item_obj.grupo != "Itens ge":
                                    var = 0
                                    for i in range(len(lista3)):
                                        if str(lista3[i][0]) == str(item_obj.pk):
                                            var = lista3[i][1]
                                    relacionamento = PaperItemAssociado()
                                    relacionamento.paper = paper
                                    relacionamento.paperItem = item_obj
                                    relacionamento.peso = item_obj.peso
                                    relacionamento.obs = var
                                    pontosComportamental = pontosComportamental - item_obj.peso
                                    relacionamento.save()
                                elif item_obj.tipo == "Venda" and str(
                                        item_obj.pk) not in listaItens and item_obj.grupo == "Erro grave" and item_obj.grupo != "Itens ge":
                                    relacionamento = PaperItemAssociado()
                                    relacionamento.paper = paper
                                    relacionamento.paperItem = item_obj
                                    relacionamento.resposta = "Sim"
                                    relacionamento.peso = 0
                                    relacionamento.save()
                                else:
                                    if item_obj.tipo == "Venda" and str(
                                            item_obj.pk) in listaItens and item_obj.grupo == "Erro grave" and item_obj.grupo != "Itens ge":
                                        var = 0
                                        for i in range(len(lista3)):
                                            if str(lista3[i][0]) == str(item_obj.pk):
                                                var = lista3[i][1]
                                        relacionamento = PaperItemAssociado()
                                        relacionamento.paper = paper
                                        relacionamento.paperItem = item_obj
                                        relacionamento.resposta = "Nao"
                                        relacionamento.peso = 0
                                        relacionamento.obs = var
                                        qterrosgraves = qterrosgraves + 1
                                        pontos = 0
                                        relacionamento.save()


            if pontos < 0:
                paper.pontos = 0
            else:
                paper.pontos = pontos
            paper.qtErrosGraves = qterrosgraves
            paper.pontosComportamental = pontosComportamental
            if pontosGe > 100:
                pontosGe = 100
            if pontosGe < 0:
                pontosGe = 0

            paper.pontosGe = pontosGe
            paper.save()
            return render(request, 'papersalvoalert.html', context= {'contestacoes':contestacoes})
        return render(request, 'papersalvoalert.html', context= {'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def usePaperNaoVenda(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        versao = VersaoPaper.objects.filter().last()
        listaLogins = []
        logins = User.objects.filter(groups__name='Vendedores', is_active=True)
        for item in logins:
            listaLogins.append(item.username)
        lista_itens = PaperItem.objects.filter(tipo="Não venda", versao=str(versao.id))
        lista_itens_proceso = lista_itens.filter(grupo="Processo", versao=str(versao.id)).order_by('cod')
        lista_itens_tecnica = lista_itens.filter(grupo="Tecnica de venda", versao=str(versao.id)).order_by('cod')
        lista_itens_comportamental = lista_itens.filter(grupo="Comportamental", versao=str(versao.id)).order_by('cod')
        lista_itensErro = lista_itens.filter(grupo="Erro grave", versao=str(versao.id)).order_by('cod')
        lista_itens_ge = lista_itens.filter(grupo="Itens ge", versao=str(versao.id)).order_by('cod')
        return render(request, 'geraPaperNãoVenda.html',
                      context={'itens': lista_itens, 'itensErro': lista_itensErro, 'processos': lista_itens_proceso,
                               "tecnicas": lista_itens_tecnica, "comportamental": lista_itens_comportamental,
                               "listaLogins": listaLogins, "lista_itens_ge": lista_itens_ge, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def createPaperNaoVenda(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        if request.method == "POST":
            listaItens = request.POST.getlist("itens")
            lista3 = []
            listaObs1 = request.POST.getlist("obs")
            listaObs = list(filter(None, (listaObs1)))

            if len(listaObs) != len(listaItens):
                return render(request, 'erroItensPendentes.html', context= {'contestacoes':contestacoes})
            for i in range(len(listaItens)):
                try:
                    listaObs[i]
                except IndexError:
                    listaObs.insert(i, "")

            for i in range(len(listaItens)):
                lista2 = [listaItens[i], listaObs[i]]
                lista3.append(lista2)

            tipo = "Não venda"
            idUser = request.POST.get("idUser")
            data = request.POST.get("dataMonitoria")
            data_ligacao = request.POST.get("data_ligacao")
            telefone = request.POST.get("telefone")
            proposta = request.POST.get("proposta")
            propostas = Paper.objects.all()
            if proposta == None:
                proposta = uuid.uuid4().hex[:6].upper()
            for item in propostas:
                if item.proposta == proposta:
                    proposta = uuid.uuid4().hex[:6].upper()

            audio = request.FILES["audio"]
            usuario = request.user.username

            if tipo:
                paper = Paper()
                paper.tipo = tipo
                paper.id_usuario = idUser
                paper.data_monitoria = data
                paper.data_ligacao = data_ligacao
                paper.telefone = telefone
                paper.proposta = proposta
                paper.audio = audio
                paper.usuario = usuario
                paper.save()
                qterrosgraves = 0
                pontos = paper.pontos
                pontosComportamental = paper.pontosComportamental
                pontosGe = paper.pontosGe
                versao = VersaoPaper.objects.filter().last()
                listaTodos = PaperItem.objects.filter(tipo="Não venda", versao_id=versao)
                cont = 0
                for item_obj in listaTodos:
                    cont +=1
                    if item_obj:
                        if item_obj.tipo == "Não venda" and str(
                                item_obj.pk) in listaItens and item_obj.grupo == "Itens ge":
                            var = 0
                            for i in range(len(lista3)):
                                if str(lista3[i][0]) == str(item_obj.pk):
                                    var = lista3[i][1]
                            relacionamento = PaperItemAssociado()
                            relacionamento.paper = paper
                            relacionamento.paperItem = item_obj
                            relacionamento.peso = item_obj.peso
                            relacionamento.obs = var
                            pontosGe = pontosGe - item_obj.peso
                            relacionamento.save()
                        if item_obj.tipo == "Não venda" and str(
                                item_obj.pk) not in listaItens and item_obj.grupo == "Itens ge":
                            relacionamento = PaperItemAssociado()
                            relacionamento.paper = paper
                            relacionamento.paperItem = item_obj
                            relacionamento.peso = 0
                            relacionamento.save()

                        if item_obj.tipo == "Não venda" and str(
                                item_obj.pk) not in listaItens and item_obj.grupo != "Comportamental" and item_obj.grupo != "Erro grave":
                            relacionamento = PaperItemAssociado()
                            relacionamento.paper = paper
                            relacionamento.paperItem = item_obj
                            relacionamento.peso = 0
                            relacionamento.save()
                        else:
                            if item_obj.tipo == "Não venda" and str(
                                    item_obj.pk) in listaItens and item_obj.grupo != "Comportamental" and item_obj.grupo != "Erro grave" and item_obj.grupo != "Itens ge":
                                var = 0
                                for i in range(len(lista3)):
                                    if str(lista3[i][0]) == str(item_obj.pk):
                                        var = lista3[i][1]
                                relacionamento = PaperItemAssociado()
                                relacionamento.paper = paper
                                relacionamento.paperItem = item_obj
                                relacionamento.peso = item_obj.peso
                                relacionamento.obs = var
                                pontos = pontos - item_obj.peso
                                relacionamento.save()
                            else:
                                if item_obj.tipo == "Não venda" and str(
                                        item_obj.pk) not in listaItens and item_obj.grupo == "Comportamental":
                                    relacionamento = PaperItemAssociado()
                                    relacionamento.paper = paper
                                    relacionamento.paperItem = item_obj
                                    relacionamento.peso = 0
                                    relacionamento.save()
                                else:
                                    if item_obj.tipo == "Não venda" and str(
                                            item_obj.pk) in listaItens and item_obj.grupo == "Comportamental":
                                        var = 0
                                        for i in range(len(lista3)):
                                            if str(lista3[i][0]) == str(item_obj.pk):
                                                var = lista3[i][1]
                                        relacionamento = PaperItemAssociado()
                                        relacionamento.paper = paper
                                        relacionamento.paperItem = item_obj
                                        relacionamento.peso = item_obj.peso
                                        relacionamento.obs = var
                                        pontosComportamental = pontosComportamental - item_obj.peso
                                        relacionamento.save()
                                    elif item_obj.tipo == "Não venda" and str(
                                            item_obj.pk) not in listaItens and item_obj.grupo == "Erro grave":
                                        relacionamento = PaperItemAssociado()
                                        relacionamento.paper = paper
                                        relacionamento.paperItem = item_obj
                                        relacionamento.resposta = "Sim"
                                        relacionamento.peso = 0
                                        relacionamento.save()
                                    else:
                                        if item_obj.tipo == "Não venda" and str(
                                                item_obj.pk) in listaItens and item_obj.grupo == "Erro grave":
                                            var = 0
                                            for i in range(len(lista3)):
                                                if str(lista3[i][0]) == str(item_obj.pk):
                                                    var = lista3[i][1]
                                            relacionamento = PaperItemAssociado()
                                            relacionamento.paper = paper
                                            relacionamento.paperItem = item_obj
                                            relacionamento.resposta = "Nao"
                                            relacionamento.peso = 0
                                            relacionamento.obs = var
                                            qterrosgraves = qterrosgraves + 1
                                            pontos = 0
                                            relacionamento.save()


                if pontos < 0:
                    paper.pontos = 0
                else:
                    paper.pontos = pontos
                paper.qtErrosGraves = qterrosgraves
                paper.pontosComportamental = pontosComportamental
                if pontosGe >100:
                    pontosGe = 100
                if pontosGe <0:
                    pontosGe = 0
                paper.pontosGe = pontosGe
                paper.save()
                return render(request, 'papersalvoalert.html', context= {'contestacoes':contestacoes})
            return render(request, 'papersalvoalert.html', context= {'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def excluir_paperIten(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        tipo = PaperItem.objects.get(id=id)
        PaperItem.objects.filter(id=id).delete()
        return redirect("/versoes")
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def geraRelatorio(request):
    contestacoes = Contestacoes.contestacoes('')
    tipos = ["Venda", "Não venda"]
    if request.user.is_superuser:
        return render(request, 'geraRelatorio.html', context={'tipos': tipos, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def gera_nova_versao(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        con = psycopg2.connect(host="localhost", database="newpaper", user="postgres", password="Baranowski25")
        cursor = con.cursor()
        versao = VersaoPaper.objects.filter().last()
        cursor.execute('SELECT * FROM public."createPaper_paperitem" where versao_id = %s', ((str(versao.id)),))

        nova_versao = VersaoPaper()
        nova_versao.versao = str(round((float(versao.versao) + float(0.1)), 5))
        nova_versao.save()
        v = nova_versao
        for row in cursor.fetchall():
            cursor.execute(
                'INSERT INTO public."createPaper_paperitem" (cod, tipo, grupo, nome, descricao, peso, "contAlteracao", resposta, obs, versao_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                (str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(0), str(row[7]),
                 str(row[8]), str(v.id)))
        con.commit()
        cursor.close()
        con.close()
        return redirect('/versoes')
    else:
        return render(request, 'erroAcessso.html' , context= {'contestacoes':contestacoes})


@login_required
def listFiltro(request):
    contestacoes = Contestacoes.contestacoes('')
    tipos = ["Venda", "Não venda"]
    if request.user.is_superuser:
        return render(request, 'listfiltro.html', context={'tipos': tipos, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def geraSelecao(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        dataI = request.POST.get("dataI")
        dataF = request.POST.get("dataF")
        papers = Paper.objects.filter(data_monitoria__range=[dataI, dataF])
        papersItens = PaperItemAssociado.objects.filter(paper_id=papers)
        return render(request, 'listPaper.html', context={'papers': papers, 'associados': papersItens, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def geraRelatorioDownload(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        dataI = request.POST.get("dataI")
        dataF = request.POST.get("dataF")
        tipo = request.POST.get("tipo")
        papers = Paper.objects.filter(data_monitoria__range=[dataI, dataF])
        if tipo == "Venda":
            linhas = []
            for paper in papers:
                if paper.tipo == "Venda":
                    paper_dict = model_to_dict(paper)
                    del paper_dict['id']
                    del paper_dict['audio']
                    del paper_dict['tipo']
                    del paper_dict['qtErrosGraves']
                    del paper_dict['usuario']
                    del paper_dict['pontosGe']

                    respostas = {}
                    respostas_comportamental = {}
                    for item in paper.paperitemassociado_set.all():
                        if item.paperItem.grupo == "Itens ge":
                            continue
                        try:
                            respostas[int(
                                item.paperItem.cod)] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                        except Exception:
                            respostas_comportamental[
                                item.paperItem.cod] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                    respostas = dict(sorted(respostas.items(), key=lambda kv: kv[0]))
                    respostas_comportamental = dict(sorted(respostas_comportamental.items(), key=lambda kv: kv[0]))
                    sorted(respostas_comportamental)
                    linhas.append({**paper_dict, **respostas, **respostas_comportamental})

            df = pd.DataFrame(linhas)
            df.to_csv('resultadovenda.csv', index=False)
            FilePointer = open('resultadovenda.csv', "r")
            response = HttpResponse(FilePointer, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultadovenda' + str(dataI) + str(dataF) + '.csv"'
            return response
        else:
            linhas = []
            for paper in papers:
                if paper.tipo == "Não venda":
                    paper_dict = model_to_dict(paper)
                    del paper_dict['id']
                    del paper_dict['audio']
                    del paper_dict['tipo']
                    del paper_dict['qtErrosGraves']
                    del paper_dict['usuario']

                    respostas = {}
                    respostas_comportamental = {}
                    for item in paper.paperitemassociado_set.all():
                        try:
                            respostas[int(
                                item.paperItem.cod)] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                        except Exception:
                            respostas_comportamental[
                                item.paperItem.cod] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                    respostas = dict(sorted(respostas.items(), key=lambda kv: kv[0]))
                    respostas_comportamental = dict(sorted(respostas_comportamental.items(), key=lambda kv: kv[0]))
                    sorted(respostas_comportamental)
                    linhas.append({**paper_dict, **respostas, **respostas_comportamental})

            df = pd.DataFrame(linhas)
            df.to_csv('resultadonaovenda.csv', index=False)
            FilePointer = open('resultadonaovenda.csv', "r")
            response = HttpResponse(FilePointer, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultadonaovenda' + str(dataI) + str(
                dataF) + '.csv"'
            return response

    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def geraRelatorioVendedor(request):
    contestacoes = Contestacoes.contestacoes('')
    tipos = ["Venda", "Não venda"]
    if request.user.is_superuser:
        return render(request, 'geraRelatorioOtimo.html', context={'tipos': tipos, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def geraRelatorioOtimoDownload(request):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        dataI = request.POST.get("dataI")
        dataF = request.POST.get("dataF")
        tipo = request.POST.get("tipo")
        papers = Paper.objects.filter(data_monitoria__range=[dataI, dataF])
        listaLogins = []
        logins = User.objects.filter(groups__name='Vendedores')
        for item in logins:
            listaLogins.append(item.username)

        if tipo == "Venda":
            linhas = []
            itensEscolhidos = []

            for i in range(len(listaLogins)):
                lista_vendedor = papers.filter(id_usuario=listaLogins[i], tipo="Venda")
                pontos = 0
                itemEscolhido = ''
                for item in lista_vendedor:
                    if item.pontos + item.pontosComportamental > pontos:
                        pontos = item.pontos + item.pontosComportamental
                        itemEscolhido = item

                itensEscolhidos.append(itemEscolhido)
            itensEscolhidos = list(filter(None, (itensEscolhidos)))
            for paper in itensEscolhidos:

                paper_dict = model_to_dict(paper)
                del paper_dict['id']
                del paper_dict['audio']
                del paper_dict['tipo']
                del paper_dict['qtErrosGraves']
                del paper_dict['usuario']
                del paper_dict['pontosGe']

                respostas = {}

                respostas_comportamental = {}
                for item in paper.paperitemassociado_set.all():
                    if item.paperItem.grupo == "Itens ge":
                        continue
                    try:
                        respostas[int(
                            item.paperItem.cod)] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                    except Exception:
                        respostas_comportamental[
                            item.paperItem.cod] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                respostas = dict(sorted(respostas.items(), key=lambda kv: kv[0]))
                respostas_comportamental = dict(sorted(respostas_comportamental.items(), key=lambda kv: kv[0]))
                sorted(respostas_comportamental)
                linhas.append({**paper_dict, **respostas, **respostas_comportamental})

            df = pd.DataFrame(linhas)
            df.to_csv('resultadovendaotimizado.csv', index=False)
            FilePointer = open('resultadovendaotimizado.csv', "r")
            response = HttpResponse(FilePointer, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultadovendaotimizado' + str(dataI) + str(
                dataF) + '.csv"'
            return response
        else:
            linhas = []
            itensEscolhidos = []

            for i in range(len(listaLogins)):
                lista_vendedor = papers.filter(id_usuario=listaLogins[i], tipo="Não venda")
                pontos = 0
                itemEscolhido = ''
                for item in lista_vendedor:
                    if item.pontos + item.pontosComportamental > pontos:
                        pontos = item.pontos + item.pontosComportamental
                        itemEscolhido = item

                itensEscolhidos.append(itemEscolhido)
            itensEscolhidos = list(filter(None, (itensEscolhidos)))

            for paper in itensEscolhidos:

                paper_dict = model_to_dict(paper)
                del paper_dict['id']
                del paper_dict['audio']
                del paper_dict['tipo']
                del paper_dict['qtErrosGraves']
                del paper_dict['usuario']

                respostas = {}
                respostas_comportamental = {}
                for item in paper.paperitemassociado_set.all():
                    try:
                        respostas[int(
                            item.paperItem.cod)] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                    except Exception:
                        respostas_comportamental[
                            item.paperItem.cod] = item.resposta if item.paperItem.grupo == "Erro grave" else item.peso
                respostas = dict(sorted(respostas.items(), key=lambda kv: kv[0]))
                respostas_comportamental = dict(sorted(respostas_comportamental.items(), key=lambda kv: kv[0]))
                sorted(respostas_comportamental)
                linhas.append({**paper_dict, **respostas, **respostas_comportamental})

            df = pd.DataFrame(linhas)
            df.to_csv('resultadonaovendaotimizado.csv', index=False)
            FilePointer = open('resultadonaovendaotimizado.csv', "r")
            response = HttpResponse(FilePointer, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="resultadonaovendaotimizado' + str(dataI) + str(
                dataF) + '.csv"'
            return response

    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def excluir_paper(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        Paper.objects.filter(id=id).delete()
        return redirect("/listpaper")
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def excluir_paper_item_associado(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        PaperItemAssociado.objects.filter(id=id).delete()

        return redirect('/listpaper')
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def editar_item_paper(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        tipos = ["Venda", "Não venda"]
        itens = PaperItem.objects.get(id=id)
        return render(request, "editarItemPaper.html", context={'itens': itens, 'tipos': tipos, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def editar_item_paper_associado(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        itens = PaperItemAssociado.objects.get(pk=id)
        return render(request, "editarItemPaperAssociado.html", context={'itens': itens, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def editar_paper(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        itens = Paper.objects.get(id=id)
        return render(request, "editarPaper.html", context={'itens': itens, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def contestar(request, id):
    contestacoes = Contestacoes.contestacoes('')
    itens = PaperItemAssociado.objects.get(pk=id)
    return render(request, "contestaitemassociado.html", context={'itens': itens, 'contestacoes':contestacoes})

@login_required
def view_paper(request, id):
    contestacoes = Contestacoes.contestacoes('')
    usuario = request.user
    if request.user:
        for item in usuario.groups.all():
            if str(item) == "Vendedores":
                itens = Paper.objects.get(id=id)
                return render(request, "viewPaper.html", context={'itens': itens, 'contestacoes':contestacoes})
    if request.user.is_superuser:
        itens = Paper.objects.get(id=id)
        cods = []
        for item in itens.paperitemassociado_set.all():
            cods.append(item.paperItem.cod)
            if cods.count(item.paperItem.cod) > 1:
                id =  item.id
                PaperItemAssociado.objects.filter(id=id).delete()
        lista = str(itens.audio).split('/')
        audio = lista[-1]
        dia = lista[-2]
        mes = lista[-3]
        ano = lista[-4]
        return render(request, "viewPaper.html", context={'itens': itens, 'audio':audio, 'dia':dia, 'mes':mes, 'ano':ano, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def view_paper_contest(request, id):
    contestacoes = Contestacoes.contestacoes('')
    usuario = request.user
    if request.user:
        for item in usuario.groups.all():
            if str(item) == "Vendedores":
                itens = Paper.objects.get(id=id)
                return render(request, "viewPapercontest.html", context={'itens': itens, 'contestacoes':contestacoes})
    if request.user.is_superuser:
        itens = Paper.objects.get(id=id)
        cods = []
        for item in itens.paperitemassociado_set.all():
            cods.append(item.paperItem.cod)
            if cods.count(item.paperItem.cod) > 1:
                id =  item.id
                PaperItemAssociado.objects.filter(id=id).delete()
        lista = str(itens.audio).split('/')
        audio = lista[-1]
        dia = lista[-2]
        mes = lista[-3]
        ano = lista[-4]
        return render(request, "viewPapercontest.html", context={'itens': itens, 'audio':audio, 'dia':dia, 'mes':mes, 'ano':ano, 'contestacoes':contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def editar_item_salvar(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        tipo = request.POST.get("tipo")
        grupo = request.POST.get("grupo")
        cod = request.POST.get("cod")
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        peso = request.POST.get("peso")
        versao = request.POST.get("versao")
        obj = VersaoPaper.objects.get(versao=versao)

        if tipo:
            itemPaper = PaperItem(id)
            itemPaper.tipo = tipo
            itemPaper.grupo = grupo
            itemPaper.cod = cod
            itemPaper.nome = nome
            itemPaper.descricao = descricao
            itemPaper.peso = peso
            itemPaper.versao = obj
            itemPaper.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def editar_item_associado_salvar(request, pk):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        obs = request.POST.get("obs")
        contestacao = request.POST.get("contestacao")
        peso = request.POST.get("peso")
        grupo = request.POST.get("grupo")
        resposta = request.POST.get("resposta")
        if resposta == None:
            resposta = ""
        contalteracao = request.POST.get("contalteracao")
        idpaper = request.POST.get("idpaper")
        idpaperItem = request.POST.get("idpaperItem")

        if peso:
            paper = Paper.objects.get(pk=idpaper)
            itemPaper = PaperItemAssociado(pk)
            usuario = request.user
            itemPeso = PaperItemAssociado.objects.get(id=pk)
            if int(itemPeso.peso) != int(peso):
                for item in usuario.groups.all():
                    if str(item) == "Operador":
                        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

            elif int(itemPeso.peso) == int(peso):
                for item in usuario.groups.all():
                    if str(item) == "Operador":
                        itemPaper.paper_id = idpaper
                        itemPaper.paperItem_id = idpaperItem
                        obs = obs
                        contestacao = contestacao
                        itemPaper.obs = obs
                        itemPaper.contestacao = contestacao
                        itemPaper.peso = peso
                        itemPaper.save()
                        paper.save()
                    return redirect('/paper/view/' + idpaper)
            itemPaper.paper_id = idpaper
            itemPaper.paperItem_id = idpaperItem
            obs = obs
            contestacao = contestacao
            itemPaper.obs = obs
            itemPaper.contestacao = contestacao
            if int(contalteracao) > itemPaper.contAlteracao:
                if grupo == "Comportamental":
                    if int(peso) == 0:
                        var = itemPaper.paper.pontosComportamental + itemPaper.paperItem.peso
                        if var > 100:
                            var = 100
                        peso = 0
                    else:
                        var = itemPaper.paper.pontosComportamental - itemPaper.paperItem.peso
                        if var > 100:
                            var = 100
                        peso = PaperItem.objects.get(id=idpaperItem).peso
                    if var < 0:
                        var = 0
                        paper.pontosComportamental = var
                    paper.pontosComportamental = var
                elif grupo == "Itens ge":
                    if int(peso) == 0:
                        var = itemPaper.paper.pontosGe + itemPaper.paperItem.peso
                        if var > 100:
                            var = 100
                        peso = 0
                    else:
                        var = itemPaper.paper.pontosGe - itemPaper.paperItem.peso
                        if var > 100:
                            var = 100
                        peso = PaperItem.objects.get(id=idpaperItem).peso
                    if var < 0:
                        var = 0
                        paper.pontosGe = var
                    paper.pontosGe = var
                else:
                    if itemPeso.resposta != resposta:
                        for item in usuario.groups.all():
                            if str(item) == "Operador":
                                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
                    if resposta != "" and resposta != "string":
                        if resposta == "Sim":
                            itemPaper.resposta = "Sim"
                            if paper.qtErrosGraves - 1 == 0 or paper.qtErrosGraves - 1 < 0:
                                pont = 0
                                for item in paper.paperitemassociado_set.all():
                                    if item.peso != 0:
                                        pont = paper.pontos + item.paperItem.peso
                                paper.pontos = 100 - pont
                                paper.qtErrosGraves = 0
                            else:
                                paper.qtErrosGraves = paper.qtErrosGraves - 1
                        elif resposta == "Nao":
                            itemPaper.resposta = "Nao"
                            var = 0
                            paper.qtErrosGraves = paper.qtErrosGraves + 1
                            paper.pontos = var
                    else:
                        if int(peso) == 0:
                            var = itemPaper.paper.pontos + itemPaper.paperItem.peso
                            peso = 0
                            if var > 100:
                                var = 100
                        else:
                            var = itemPaper.paper.pontos - itemPaper.paperItem.peso
                            peso = PaperItem.objects.get(id=idpaperItem).peso
                        if var < 0:
                            var = 0
                            paper.pontos = var
                        paper.pontos = var

                if paper.qtErrosGraves > 0:
                    paper.pontos = 0
                itemPaper.peso = peso
                itemPaper.save()
                paper.save()
                return redirect('/paper/view/' + idpaper)
            else:
                return redirect('/paper/view/' + idpaper)
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def salvar_contestacao(request, pk):
    contestacoes = Contestacoes.contestacoes('')
    idpaper = request.POST.get("idpaper")
    obs = request.POST.get("obs")
    peso = request.POST.get("peso")
    contestacao = request.POST.get("contestacao")
    idpaperItem = request.POST.get("idpaperItem")
    paper = Paper.objects.get(pk=idpaper)
    itemPaper = PaperItemAssociado(pk)
    usuario = request.user
    data = datetime.now()
    dia = data.day
    if (int(paper.data_monitoria.day)) <= (int(int(dia) + 2)):
        if str(usuario) == str(paper.id_usuario):
            itemPaper.paper_id = idpaper
            itemPaper.paperItem_id = idpaperItem
            itemPaper.contestacao = contestacao
            obs = obs
            itemPaper.peso = peso
            itemPaper.obs = obs
            itemPaper.save()
            paper.save()
            return redirect('/paper/view/' + idpaper)
    elif (int(paper.data_monitoria.day)) > (int(int(dia) + 2)):
        return render(request, 'erroDiacontestacao.html', context={'contestacoes': contestacoes})
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})

@login_required
def editar_paper_salvar(request, id):
    contestacoes = Contestacoes.contestacoes('')
    if request.user.is_superuser:
        usuario = request.user
        for item in usuario.groups.all():
            if str(item) == "Operador":
                return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})
        vendedor = request.POST.get("vendedor")
        telefone = request.POST.get("telefone")
        erros = request.POST.get("errosGraves")
        pontosge = request.POST.get("pontosGe")
        pontos = request.POST.get("pontos")
        pontoscomportamental = request.POST.get("pontosComportamental")
        data = request.POST.get("data")
        proposta = request.POST.get("proposta")
        try:
            audio = request.FILES["audio"]
        except KeyError:
            paper = Paper.objects.get(id=id)
            audio = paper.audio

        if telefone:
            paper = Paper.objects.get(id=id)
            paper.id_usuario = vendedor
            paper.telefone = telefone
            paper.pontosGe = pontosge
            paper.pontos = pontos
            paper.pontosComportamental = pontoscomportamental
            paper.qtErrosGraves = erros
            if int(erros) > 0:
                paper.pontos = 0
            elif int(erros) == 0:
                pont = 0
                for item in paper.paperitemassociado_set.all():
                    if item.peso != 0:
                        pont = int(paper.pontos) + item.paperItem.peso
                paper.pontos = abs(100 - pont)

            paper.data_monitoria = data
            paper.proposta = proposta
            if str(paper.audio) != str(audio):
                audio = request.FILES["audio"]
                paper.audio = audio
                paper.save()
            else:
                paper.save()
            return redirect('/listpaper')
    else:
        return render(request, 'erroAcessso.html', context= {'contestacoes':contestacoes})


@login_required
def download_gravacao(request, id):
    #if request.user.is_superuser:
        paper = Paper.objects.get(id=id)
        FilePointer = paper.audio
        response = HttpResponse(FilePointer, content_type='application/mp3')
        response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response
    #else:
        #return render(request, 'erroAcessso.html')
