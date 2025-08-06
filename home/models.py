from django.db import models


class Cliente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    cpf = models.CharField(unique=True, max_length=11)

    class Meta:
        managed = False
        db_table = 'cliente'
        
    def __str__(self):
        return self.nome


class Evento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45)
    capacidade_pessoas = models.IntegerField()
    imagem = models.ImageField(upload_to="eventos")
    descricao = models.TextField()
    data = models.DateTimeField(unique=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evento'
    
    def __str__(self):
        return self.nome


class Ingresso(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_ID')  # Field name made lowercase.
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='Evento_ID')  # Field name made lowercase.
    id_ingresso = models.CharField(db_column='ID_ingresso', primary_key=True, max_length=45)  # Field name made lowercase.
    setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='setor_ID')  # Field name made lowercase.
    data_emissao = models.DateTimeField()
    status = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'ingresso'
    
    def __str__(self):
        return f"Ingresso para o cliente {self.cliente.nome} no evento {self.evento.nome}"


class Perfil(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perfil'
        
    def __str__(self):
        return self.nome


class Setor(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45)
    quantidade_ingresso = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='Evento_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'setor'
        
    def __str__(self):
        return self.nome


class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    cpf = models.CharField(unique=True, max_length=14)
    senha = models.CharField(max_length=250)
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='Perfil_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'
        
    def __str__(self):
        return self.nome
