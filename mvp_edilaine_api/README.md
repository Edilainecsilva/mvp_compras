# Edilaine API - MVP

Este é um MVP que foi solicitado no curso de Desenvolvimento Full Stack da PUC RIO, referente a Disciplina: Sprint I: Desenvolvimento Full Stack Básico. Foi solicitado para cada aluno criar o seu próprio MVP. O meu MVP trata-se de uma API refente ao cadastro, vizualização e remocão de dados de Compras efetuadas, com Lojas relacionadas a essas compras. O MVP foi criado utilizando a linguagem Pyhton com Flask, SQLAlchemy e Sqlite3, utilizando também Html, Java Script, CSS e JSON. Foram criados dois projetos separados: sendo um para a API e outro para o front-end.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
