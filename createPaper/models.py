from django.contrib.auth.models import User
from django.db import models


class VersaoPaper(models.Model):
    versao = models.CharField('versao', max_length=150, default="1.0")

    def __str__(self):
        return self.versao


class PaperItem(models.Model):
    cod = models.CharField('cod', max_length=150, default="string")
    tipo = models.CharField('tipo', max_length=150)
    grupo = models.CharField('grupo', max_length=50)
    nome = models.CharField('nome', max_length=550, default='string')
    descricao = models.TextField('descricao', max_length=550, default='string')
    peso = models.IntegerField('peso')
    resposta = models.CharField('cod', max_length=150, default="")
    obs = models.CharField('obs', max_length=550, default="")
    contestacao = models.TextField('contestacao', default="")
    contAlteracao = models.IntegerField('contalteracao', default=0)
    versao = models.ForeignKey(VersaoPaper, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Paper(models.Model):
    tipo = models.CharField('tipo', max_length=150)
    id_usuario = models.CharField('id_usuario', max_length=50)
    data_monitoria = models.DateField('data_monitoria', default=None)
    data_ligacao = models.DateField('data_ligacao', blank=True, null=True)
    telefone = models.CharField('telefone', max_length=50, default='string')
    proposta = models.TextField('proposta', max_length=550, default='string', unique=True)
    pontos = models.IntegerField('pontos', default=100)
    pontosComportamental = models.IntegerField('pontos_comportamental', default=100)
    pontosGe = models.IntegerField('pontos_ge', default=100)
    qtErrosGraves = models.IntegerField('qterrosgraves', default=0)
    audio = models.FileField('audio', upload_to='core/static/media/%Y/%m/%d/', default='string')
    usuario = models.CharField('usuario', max_length=150, default=None)

    def __str__(self):
        return self.tipo


class PaperItemAssociado(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    paperItem = models.ForeignKey(PaperItem, on_delete=models.PROTECT)
    peso = models.IntegerField('peso')
    resposta = models.CharField('cod', max_length=150, default="")
    obs = models.TextField('obs', default="")
    contestacao = models.TextField('contestacao', default="")
    contAlteracao = models.IntegerField('contalteracao', default=0)
