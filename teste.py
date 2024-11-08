import typer
import requests #pede acesso ao api

API_KEY = '71c6f8366ef375e8b61b33a56a2ce9d9'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', #engana o api a pensar que estou a aceder pro um navegador
}

def response(): #função para fazer a requisição
    url = f'https://api.itjobs.pt/job/list.json?api_key={API_KEY}'
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

app = typer.Typer()

@app.command()
def top(n: int, csv: bool = False):
    """ Lista os N trabalhos mais recentes publicados pela itjobs.pt """
    #argumento opcional para csv
    jobs = []
    page = 1
    while len(jobs) < n:
        data = response()
        jobs += data['results']
        page += 1
        if not data['results']: 
            break
    jobs = jobs[:n]
    for x in jobs:
       title = x.get('title', 'NA') #se não existir valor em 'title' apresenta 'NA'
       company_name = x.get('company', {}).get('name', 'NA')
       body = x.get('body', 'NA')
       published_at = x.get('publishedAt', 'NA')
       try: #tenta aceder ao index 0 da lista, se não existir retorna 'NA'
           location = x['locations'][0].get('name', 'NA') 
       except (IndexError, KeyError): 
           location = 'NA'
       wage = x.get('wage', 'NA')
       print(f"Título: {title}")
       print(f"Empresa: {company_name}")
       print(f"Description: {body}")
       print(f"Data de publicação: {published_at}")
       print(f"Location: {location}")
       print(f"Salário: {wage}")
    #if csv:
        #código para criar ficheiro csv com as respostas
        #titulo;empresa;descricao;data de publicacao;salario;localizacao
    #else:
        #break
#kshbcksjbcslj
@app.command()
def search(nome: str, localidade: str, n: Annotated[Optional[int], typer.Argument()]=None, csv: bool = False):
    """ Lista todos os trabalhos full-time publicados por uma determminada empresa, numa determinada região """
    data = response()
    jobs += data['results']
    jobs_full_time = (data['company']['name']== nome and data['types'][0]["name"]== "Full-time" and data['locations']==['locations'][0]['name']== localidade)
    if n is not None:
        jobs_full_time = jobs_full_time[:n]
        for x in jobs_full_time:
            title = x.get('title', 'NA') #se não existir valor em 'title' apresenta 'NA'
            company_name = x.get('company', {}).get('name', 'NA')
            body = x.get('body', 'NA')
            published_at = x.get('publishedAt', 'NA')
            try: #tenta aceder ao index 0 da lista, se não existir retorna 'NA'
                location = x['locations'][0].get('name', 'NA') 
            except (IndexError, KeyError): 
                location = 'NA'
            wage = x.get('wage', 'NA')
            print(f"Título: {title}")
            print(f"Empresa: {company_name}")
            print(f"Description: {body}")
            print(f"Data de publicação: {published_at}")
            print(f"Location: {location}")
            print(f"Salário: {wage}")

    else:
        for x in jobs_full_time:
            title = x.get('title', 'NA') #se não existir valor em 'title' apresenta 'NA'
            company_name = x.get('company', {}).get('name', 'NA')
            body = x.get('body', 'NA')
            published_at = x.get('publishedAt', 'NA')
            try: #tenta aceder ao index 0 da lista, se não existir retorna 'NA'
                location = x['locations'][0].get('name', 'NA') 
            except (IndexError, KeyError): 
                location = 'NA'
            wage = x.get('wage', 'NA')
            print(f"Título: {title}")
            print(f"Empresa: {company_name}")
            print(f"Description: {body}")
            print(f"Data de publicação: {published_at}")
            print(f"Location: {location}")
            print(f"Salário: {wage}")


    #tem que permitir inserir o número de traablhos a apresentar, caso contrário apresenta todos os trabalhos
    #argumento opcional para csv

@app.command()
def salary(n: int):
    """ Extrai a informação relativa ao salário oferecido por uma determinado job id """
    #mesmo que o valor seja 'wage a null'; neste caso usar expressões regulares para procurar noutros campos relevantes

@app.command()
def skills(n:int):
    """ Quais os trabalhos que requerem uma determinada lista de skills, num determinado período de tempo """
    #recebe a lista de skills e datas de início e de fim [skill1, skill2, skill3] dataInicial dataFinal
    #argumento opcional para csv

#para cada funcionalidade (exceto salary), deve poder exportar para CSV a informação com os campos: título, empresa, descrição, data de publicação, salário e localização
#para isso, é necessário poder adicionar um argumento opcional a cada um dos comandos

if __name__ == "__main__":
    app()