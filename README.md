
# Senac Music Hall

Sistema voltado ao gerenciamento e organização da grade de eventos no Senac Music Hall, onde será a função de cadastrar eventos com seus respectivos setores e também gerenciar a venda dos ingressos. Também o sistema terá uma parte voltada a validação de ingressos e também dando um dashboard com gráficos mostrando o andamento das vendas dos ingressos

## Funcionalidades

- Cadastro de funcionários
- Separação dos funcionários por perfil de acesso
- Cadastro de eventos
- Cadastro de setores por evento
- Exibição de eventos para acontecer
- Venda e emissão de ingressos por evento
- Validação e cancelamento de ingressos emitidos
- Dashboard administrativos com gráfico mostrando a venda de cada evento

## Screenshots

![App Screenshot](/home/static/img/img.png)


## Instalação

Crie um ambiente virtual python usando comando

```bash
    virtualenv venv
```

Inicie o ambiente virtual no terminal

```bash
    venv/Scripts/Activate
```

Instale o requirements.txt presente no repositório onde contém os pacotes necessários para o sistema rodar

```bash
    pip install -r requirements.txt
```

Rode o sistema em sua máquina local

```bash
    python manage.py runserver
```


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`SECRET_KEY`

`NAME_DATABASE`

`USER_DATABASE`

`PASSWORD_DATABASE`

`HOST_DATABASE`

`PORT_DATABASE`


## Documentação

- [Prototipo figma](https://www.figma.com/proto/wLjtMZpx77lg6vGdT1aGcV/Senac-Music-Hall?node-id=330-1279&t=KMKMP1Gu6dk7Oa2e-1&scaling=contain&content-scaling=fixed&page-id=330%3A716&starting-point-node-id=330%3A1279&show-proto-sidebar=1)



