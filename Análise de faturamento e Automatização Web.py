import pandas as pd
import win32com.client

# importar a base de dados
tabela_vendas = pd.read_excel("C:\\Users\Gabri\Downloads\Vendas.xlsx")

# visualizar a base de dados
pd.set_option('display.max_columns', None)
print(tabela_vendas)

# faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

# quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)

print('-' * 50)
# ticket médio por produto em cada loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)

# enviar um email com o relatório
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)
mail.To = 'gabrielferreiradevp.com' #EMAIL DO DESTINATARIO
mail.Subject = 'Relatório de Vendas por Loja' #TITULO DO EMAIL
mail.HTMLBody = f''' 
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Gabriel F.</p>
'''#conteudo do email com a mensagem formatada

mail.Send()
print('='*20)
print('Email Enviado')