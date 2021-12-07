import PySimpleGUI as sg




#Esta função calcula o IRRF
def leao(base_irrf, num_dependente):
    '''Esta função calcula o imposto de renda retido na fonte baseado no salário
     bruto sem benefícios não tributáveis e com a dedução do regime de previdência'''

    imposto = 0
    #faixas de imposto com cálculo de dedução
    if base_irrf <= 1903.98:
        imposto = -189.59*num_dependente

    if base_irrf >= 1903.99 and base_irrf <= 2826.65:
        imposto = base_irrf*0.075 - 142.8 -189.59*num_dependente

    if base_irrf >= 2826.66 and base_irrf <= 3751.05:
        imposto = base_irrf*0.15 - 354.8 -189.59*num_dependente

    if base_irrf >= 3751.06 and base_irrf < 4664.68:
        imposto = base_irrf*0.225 - 636.13 -189.59*num_dependente

    if base_irrf >= 4664.68:
        imposto = base_irrf*0.275 - 869.36 -189.59*num_dependente

    return imposto
#esta função calcula o desconto do INSS para os profs temporarios
def INSS(salario_bruto):

    inss = 0

    if salario_bruto <= 1100:
        inss = salario_bruto*0.075
    if salario_bruto >= 1100.01 and salario_bruto <= 2203.48:
        inss = (salario_bruto - 1100.01)*0.09 + 82.5
    if salario_bruto >= 2203.49 and salario_bruto <= 3305.22:
        inss = (salario_bruto - 2203.49)*0.12 + 181.81
    if salario_bruto >= 3305.23 and salario_bruto <= 6433.57:
        inss = (salario_bruto - 3305.23)*0.14 + 314.02
    if salario_bruto > 6433.57:
        inss = 751.99
    return inss

def salario_temporario(num_dependente, substituição, vencimento_base, jornada_base, alimentacao):

    aprimoramento = 500


    imposto = previdencia = salario_bruto = salario_liquido = 0

    if substituição == 0:

        salario_bruto = vencimento_base + alimentacao

    else:

        salario_bruto = vencimento_base + vencimento_base*(substituição/jornada_base) + alimentacao

    previdencia = INSS(salario_bruto)

    base_irrf = salario_bruto - previdencia - alimentacao

    imposto = leao(base_irrf, num_dependente)

    salario_liquido = salario_bruto - previdencia - imposto + aprimoramento

    return salario_liquido

def salario_efetivo(num_dependente, substituição, letra, vencimento_base, gratificacao_mestrado, jornada_base, alimentacao):

    aprimoramento = 500

    imposto = previdencia = salario_bruto = salario_liquido = 0

    if substituição == 0:

        salario_bruto = vencimento_base

    else:

        salario_bruto = vencimento_base + vencimento_base*(substituição/jornada_base) + gratificacao_mestrado

    previdencia = (vencimento_base + gratificacao_mestrado)*0.1425

    base_irrf = salario_bruto - previdencia

    imposto = leao(base_irrf, num_dependente)

    salario_liquido = salario_bruto - previdencia - imposto + aprimoramento + alimentacao

    return salario_liquido

def conversor_letra(h_letra):
    if h_letra == 'A':
        letra = 0
    if h_letra == 'B':
        letra = 1
    if h_letra == 'C':
        letra = 2
    if h_letra == 'D':
        letra = 3
    if h_letra == 'E':
        letra = 4
    if h_letra == 'F':
        letra = 5
    if h_letra == 'G':
        letra = 6
    return letra
#layout
layout = [
    [sg.Text('Bem-vindo à calculadora de salário dos professores da SEDUC GO!')],
    [sg.Text('Esta versão do programa *NÃO* inclui no cálculo de salário:')],
    [sg.Text('===> Quinquênio')],
    [sg.Text('===> Bônus por Resultado ou Bônus Fundeb')],
    [sg.Text('===> GDPI')],
    [sg.Text('Carga horária base: '), sg.Combo(['20 horas', '30 horas', '40 horas'], key='carga_horaria', size=(8, 1))],
    [sg.Text('Nº de aulas de complementação da carga horária: '), sg.Spin([i for i in range(0, 15)], initial_value=0, key='complementacao', size=(2, 1))],
    [sg.Text('Tem auxílio internet de 100 reais? '), sg.Radio('Sim', 'internet', key='tem_100'), sg.Radio('Não', 'internet', key='n_tem_100')],
    [sg.Text('Você tem quantos dependentes ?'), sg.Spin([i for i in range(0, 21)], initial_value=0, key='n_dep', size=(2, 1))],
    [sg.Text('Você é sindicalizado? '), sg.Radio('Sim', 'sindicato', key='eh_sind'), sg.Radio('Não', 'sindicato', key='n_eh_sind')],
    [sg.Text('O seu vínculo é:'), sg.Radio('Efetivo', 'vinculo', key='eh_efetivo'), sg.Radio('Temporário', 'vinculo', key='eh_temporario')],
    [sg.Text('Caso tenha vínculo Efetivo, marque as opções abaixo')],
    [sg.Text('Você é: '), sg.Radio('P3', 'posicao_vertical', key='eh_p3'), sg.Radio('P4', 'posicao_vertical', key='eh_p4')],
    [sg.Text('Sua letra é: '), sg.Combo(['A', 'B', 'C', 'D', 'E', 'F', 'G'], key='h_letra')],
    [sg.Text('Você possui mestrado? '), sg.Radio('Sim', 'p_mestrado', key='tem_mestrado'), sg.Radio('Não', 'p_mestrado', key='n_tem_mestrado')],
    [sg.Output(size=(63, 10))],
    [sg.Button('Calcular!'), sg.Button('Sair')]
]
#janela
window = sg.Window('Calculadora de Salário GUI version 1.0 by Gustavo B. Franz', layout, icon=r'D:\Calculadora Salário\Versão GUI\Flag_of_Goias.ico')

while True:
    evento, valores = window.read()
    if evento is None or evento == 'Sair':
        break
    carga_horaria = valores['carga_horaria']
    complementacao = valores['complementacao']
    tem_internet = valores['tem_100']
    num_dependente = valores['n_dep']
    eh_efetivo = valores['eh_efetivo']
    eh_p3 = valores['eh_p3']
    eh_p4 = valores['eh_p4']
    h_letra = valores['h_letra']
    tem_mestrado = valores['tem_mestrado']
    é_sindicalizado = valores['eh_sind']


    #variaveis globais
    vencimento_base = sintego = internet = alimentacao = ch_base = 0

    #coleta o valor da carga horária básica
    if carga_horaria == '20 horas':
        ch_base = 20
    if carga_horaria == '30 horas':
        ch_base = 30
    if carga_horaria == '40 horas':
        ch_base = 40

    #calcula o número de aulas correspondente à carga horaria informada e converte para o código correspondente da CRE
    jornada_base = round((ch_base*0.7)*7.51)


    substituição = round(complementacao*7.51)

    if tem_internet:
        internet = 100

    if eh_efetivo:

        #listas abaixo contém o valor do vencimento base de acordo com a carga horaria (linhas) e letra (colunas)
        p3 = [[1789.84, 1825.63, 1862.15, 1899.40, 1937.38, 1976.12, 2015.64], [2684.74, 2738.45, 2793.23, 2849.09, 2906.07, 2964.19, 3023.47], [3579.68, 3651.25, 3724.29, 3798.78, 3874.76, 3952.25, 4031.29]]
        p4 = [[2018.05, 2058.41, 2099.57, 2141.56, 2184.40, 2228.08, 2272.64], [3027.07, 3087.61, 3149.35, 3212.34, 3276.58, 3342.11, 3408.95], [4036.09, 4116.81, 4199.13, 4283.12, 4368.78, 4456.15, 4545.28]]
        #coleta info acerca da posição vertical do prof na carreira


        if eh_p3:

            if carga_horaria == '20 horas':

                vencimento_base = p3[0]

                alimentacao = 250

            if carga_horaria == '30 horas':

                vencimento_base = p3[1]

                alimentacao = 500

            if carga_horaria == '40 horas':

                vencimento_base = p3[2]

                alimentacao = 500

        if eh_p4:

            if carga_horaria == '20 horas':

                vencimento_base = p4[0]

                alimentacao = 250

            if carga_horaria == '30 horas':

                vencimento_base = p4[1]

                alimentacao = 500

            if carga_horaria == '40 horas':

                alimentacao = 500

                vencimento_base = p4[2]

        #coleta info acerca do posição horizontal do prof na carreira
        letra = conversor_letra(h_letra)

        vencimento_base = vencimento_base[letra]

        #coleta info sobre mestrado do prof
        gratificacao_mestrado = 0

        if tem_mestrado:

            gratificacao_mestrado = vencimento_base*0.4

        if é_sindicalizado:

            sintego = vencimento_base*0.01


        #calcula o salario liquido do efetivo
        salario_liquido = salario_efetivo(num_dependente, substituição, letra, vencimento_base, gratificacao_mestrado, jornada_base, alimentacao) - sintego + internet

        print('\nO seu salário líquido é de R$', salario_liquido)
        print('\nPapai Caiado não está pagando mal hein ( ͡° ͜ʖ ͡°)')


    else:

        ptemp = [1508.31, 2262.45, 3016.60]

        if carga_horaria == '20 horas':

            vencimento_base = ptemp[0]

            alimentacao = 250

        if carga_horaria == '30 horas':

            vencimento_base = ptemp[1]

            alimentacao = 500

        if carga_horaria == '40 horas':

            vencimento_base = ptemp[2]

            alimentacao = 500

        if é_sindicalizado:

            sintego = vencimento_base*0.01

        #calcula o salario liquido do temporario
        salario_liquido = salario_temporario(num_dependente, substituição, vencimento_base, jornada_base, alimentacao) - sintego + internet

        print('\nO seu salário líquido é de R$', salario_liquido)
        print('\nPapai Caiado não está pagando mal hein ( ͡° ͜ʖ ͡°)')
