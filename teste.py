import typer
import requests #pede acesso ao api
from typing import Optional
import json

API_KEY = '71c6f8366ef375e8b61b33a56a2ce9d9'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', #engana o api a pensar que estou a aceder pro um navegador
}

def response(page): #função para fazer a requisição
    url = f'https://api.itjobs.pt/job/list.json?api_key={API_KEY}&page={page}'
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

app = typer.Typer()

@app.command()
def top(n: int, csv: bool = False):
    """ Lista os N trabalhos mais recentes publicados pela itjobs.pt """
    #argumento opcional para csv

@app.command()
def search(nome: str, localidade: str, n: Optional[int] = None, csv: bool = False):
    """ Lista todos os trabalhos full-time publicados por uma determminada empresa, numa determinada região. Insira o nome da empresa e da localidade entre aspas para melhor funcionamento. """
    jobs_full_time = []
    page = 1
    while True:
        data = response(page)
        for job in data['results']: 
            company_name = job.get('company',{}).get('name', None) #dicionário então {}; valor então None
            if company_name == nome:
                types = job.get('types',[{}])  #lista de dicionários então [{}]
                if types[0].get('name') == 'Full-time':
                    locations = job.get('locations', [{}]) #lista de dicionários então  [{}]
                    if any(location.get('name', None) == localidade for location in locations): #valor então None
                        jobs_full_time.append(job)
        page += 1
        if 'results' not in data:
            break
    if n is not None:
        jobs_full_time = jobs_full_time[:n]
    output = []
    for job in jobs_full_time:
        job_info = {
            "Título": job.get('title', 'NA'),
            "Empresa": job.get('company', {}).get('name', 'NA'),
            "Descrição": (job.get('body', 'NA')[:200] + '...') if len(job.get('body', 'NA')) > 200 else job.get('body', 'NA'),
            "Data de publicação": job.get('publishedAt', 'NA'), 
            "Localização": job['locations'][0].get('name', 'NA') if job.get('locations') else 'NA', 
            "Salário": job.get('wage', 'NA')
        }
        output.append(job_info)
    if output:
        print(json.dumps(output, indent=4, ensure_ascii=False))
    else:
        print("Não foram encontradas correspondências para a sua pesquisa.")

#if csv:
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