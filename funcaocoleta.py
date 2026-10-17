"""
MÓDULO DE INTERFACE E COLETA DE DADOS (interface.py)

Este módulo gerencia a comunicação direta com o usuário via terminal.
Ele realiza loops de input, exibe mensagens, trata erros amigavelmente 
e consome as regras puras de validação do módulo 'funcaoregra'.

Como utilizar:
    >>> from interface import pedir_sexo, pedir_cpf, cadastrar_endereco
    >>> documento = pedir_cpf()
"""

from time import sleep
from typing import Any, Dict, Optional
import requests

# Importação das regras matemáticas e de validação puras
try:
    from funcaoregra import (
        calcular_idade,
        consultar_cep,
        validar_cartao,
        validar_cpf,
        validar_telefone,
    )
except (ImportError, ModuleNotFoundError):
    from .funcaoregra import (
        calcular_idade,
        consultar_cep,
        validar_cartao,
        validar_cpf,
        validar_telefone,
    )


# ==============================================================================
# ELEMENTOS VISUAIS E UTILITÁRIOS
# ==============================================================================

def lin(tamanho: int = 50, caractere: str = '-=') -> None:
    """
    Imprime uma linha divisória visual no terminal para organizar saídas e cabeçalhos.

    Args:
        tamanho (int): Quantidade de repetições do caractere (padrão: 50).
        caractere (str): Sequência de caracteres para formar a linha (padrão: '-=').

    Exemplo:
        >>> lin(15, '=')
        ===============
    """
    print(caractere * tamanho)


def exibir_cabecalho(titulo: str) -> None:
    """
    Exibe um título centralizado entre linhas divisórias.

    Args:
        titulo (str): Texto a ser exibido no centro.
    """
    lin(30, '=')
    print(f'{titulo.center(60)}')
    lin(30, '=')


# ==============================================================================
# COLETA DE DADOS BÁSICOS (MENUS E SELEÇÕES)
# ==============================================================================

def pedir_sexo() -> str:
    """
    Apresenta um menu interativo no terminal para seleção de sexo/gênero.
    Garante que o usuário escolha apenas opções válidas.

    Returns:
        str: 'Feminino' ou 'Masculino'.

    Exemplo de saída no terminal:
        >>> pedir_sexo()
        [1] Feminino
        [2] Masculino
        Escolha uma opção: 1
        'Feminino'
    """
    opcoes = {
        '1': 'Feminino',
        '2': 'Masculino',
    }

    while True:
        print('\nSelecione o Sexo:')
        print('  [1] Feminino')
        print('  [2] Masculino')
        opcao = input('Opção: ').strip()

        if opcao in opcoes:
            return opcoes[opcao]

        print('-> Opção inválida! Digite apenas 1 ou 2.')
        sleep(0.5)


def pedir_estado_civil() -> str:
    """
    Apresenta menu numérico para seleção de estado civil e valida a entrada.

    Returns:
        str: Descrição do estado civil selecionado.

    Exemplo:
        'Solteiro(a)', 'Casado(a)', etc.
    """
    opcoes = {
        '1': 'Solteiro(a)',
        '2': 'Casado(a)',
        '3': 'Separado(a)',
        '4': 'Divorciado(a)',
        '5': 'Viúvo(a)',
    }

    while True:
        print('\nSelecione o Estado Civil:')
        print('  [1] Solteiro(a)')
        print('  [2] Casado(a)')
        print('  [3] Separado(a)')
        print('  [4] Divorciado(a)')
        print('  [5] Viúvo(a)')
        opcao = input('Opção: ').strip()

        if opcao in opcoes:
            return opcoes[opcao]

        print('-> Opção inválida! Digite um número de 1 a 5.')
        sleep(0.5)


def exibir_menu_navegacao() -> int:
    """
    Apresenta um menu básico de navegação para continuidade ou saída do programa.

    Returns:
        int: Código da opção escolhida (1 para sair, 2 para voltar ao menu principal).
    """
    while True:
        print('\nNavegação:')
        print('  [1] Sair do sistema')
        print('  [2] Voltar ao menu principal')
        opcao = input('Opção: ').strip()

        if opcao == '1':
            print('Encerrando programa...')
            exit(0)
        elif opcao == '2':
            return 2

        print('-> Opção inválida! Escolha 1 ou 2.')


# ==============================================================================
# COLETA E VALIDAÇÃO DE DADOS PESSOAIS
# ==============================================================================

def pedir_data_nascimento() -> int:
    """
    Solicita a data de nascimento no terminal, valida a existência e calcula a idade.

    Consome:
        funcaoregra.calcular_idade()

    Returns:
        int: Idade calculada em anos inteiros.
    """
    while True:
        entrada = input('\nData de nascimento (DD/MM/AAAA): ').strip()
        try:
            idade = calcular_idade(entrada)
            print(f'-> Data aceita! Idade calculada: {idade} anos.')
            return idade
        except ValueError as erro:
            print(f'-> Entrada inválida: {erro}. Tente novamente.')


def pedir_cpf() -> Optional[str]:
    """
    Solicita o CPF no console em loop. Permite encerramento com 'sair'.

    Consome:
        funcaoregra.validar_cpf()

    Returns:
        Optional[str]: CPF formatado (XXX.XXX.XXX-XX) ou None se cancelado.
    """
    while True:
        entrada = input("\nDigite o CPF (ou 'sair' para cancelar): ").strip()

        if entrada.lower() == 'sair':
            print('-> Coleta de CPF cancelada.')
            return None

        cpf_formatado = validar_cpf(entrada)
        if cpf_formatado:
            print(f'-> CPF válido e registrado: {cpf_formatado}')
            return cpf_formatado

        print('-> CPF inválido (dígitos verificadores incorretos). Tente novamente.')


def pedir_endereco() -> Optional[Dict[str, str]]:
    """
    Conduz o fluxo completo de cadastro de endereço consultando a API do ViaCEP.
    Preenche rua, bairro, cidade e UF automaticamente e solicita número e complemento.

    Consome:
        funcaoregra.consultar_cep()

    Returns:
        Optional[Dict[str, str]]: Dados completos com endereço formatado ou None se falhar.
    """
    print('\n=== CADASTRO DE ENDEREÇO ===')
    cep_digitado = input('Digite o CEP (com ou sem máscara): ').strip()

    try:
        dados_cep = consultar_cep(cep_digitado)
    except (ValueError, requests.RequestException) as erro:
        print(f'-> Falha ao processar CEP: {erro}')
        return None

    if not dados_cep:
        print('-> CEP não encontrado na base de dados dos Correios.')
        return None

    print(f"-> Localizado: {dados_cep['cidade']}/{dados_cep['uf']}")

    # Se a API não retornar logradouro ou bairro, solicita ao usuário
    rua = dados_cep['rua'] or input('Rua/Logradouro não informado pela base. Digite: ').strip()
    bairro = dados_cep['bairro'] or input('Bairro não informado pela base. Digite: ').strip()
    cidade = dados_cep['cidade']
    uf = dados_cep['uf']

    numero = input('Digite o número da residência: ').strip()
    complemento = input('Complemento (Apto, Bloco, etc. - opcional): ').strip()

    comp_texto = f', {complemento}' if complemento else ''
    endereco_completo = f'{rua}, Nº {numero}{comp_texto} - {bairro}, {cidade}/{uf}'

    print(f'\nEndereço registrado: {endereco_completo}')

    return {
        'cep': dados_cep['cep'],
        'rua': rua,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'cidade': cidade,
        'uf': uf,
        'endereco_formatado': endereco_completo,
    }


def pedir_telefone() -> Optional[Dict[str, str]]:
    """
    Solicita o número de telefone no terminal e valida usando libphonenumber.

    Consome:
        funcaoregra.validar_telefone()

    Returns:
        Optional[Dict[str, str]]: Dicionário com número formatado e localidade ou None se inválido.
    """
    entrada = input('\nDigite o telefone com DDD (ou DDI, ex: +55 21 98470-9360): ').strip()
    resultado = validar_telefone(entrada)

    if resultado:
        print(f"-> Telefone válido ({resultado['origem']}): {resultado['telefone_internacional']}")
        return resultado

    print('-> Número de telefone inválido ou incompleto.')
    return None


def pedir_cartao() -> Optional[Dict[str, str]]:
    """
    Solicita o número do cartão, valida via algoritmo de Luhn e identifica a bandeira.

    Consome:
        funcaoregra.validar_cartao()

    Returns:
        Optional[Dict[str, str]]: Dicionário com 'bandeira' e 'numero_mascarado' ou None se inválido.
    """
    entrada = input('\nDigite o número do cartão (apenas números ou com espaços): ').strip()
    resultado = validar_cartao(entrada)

    if resultado:
        print('-> Cartão válido!')
        print(f"   Bandeira: {resultado['bandeira']}")
        print(f"   Número: {resultado['numero_mascarado']}")
        return resultado

    print('-> Cartão inválido (falha no dígito verificador ou tamanho incompatível).')
    return None