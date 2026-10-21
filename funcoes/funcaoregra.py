"""
MÓDULO DE REGRAS DE NEGÓCIO E VALIDAÇÕES (regras.py)

Este módulo contém apenas funções puras de processamento, cálculo e validação.
Nenhuma função aqui interage com o terminal (sem input() ou print()).

Como utilizar:
    Basta importar as funções necessárias em qualquer outro script, API ou pipeline:
    >>> from regras import calcular_idade, validar_cpf, consultar_cep
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional
import phonenumbers
from phonenumbers import NumberParseException, geocoder
import requests
from validate_docbr import CPF


# ==============================================================================
# 1. CÁLCULO DE IDADE
# ==============================================================================

def calcular_idade(data_nascimento_str: str) -> int:
    """
    Calcula a idade exata em anos a partir de uma data de nascimento em texto.

    Como usar:
        Passe uma string com a data no padrão 'DD/MM/AAAA'. A função compara
        com a data atual do sistema, ajustando o resultado caso o aniversário
        ainda não tenha ocorrido no ano vigente.

    Args:
        data_nascimento_str (str): Data de nascimento formatada como 'DD/MM/AAAA'
                                   (ex: '24/11/2006'). Espaços extras nas pontas
                                   são removidos automaticamente.

    Returns:
        int: Idade calculada em anos completos.

    Raises:
        ValueError: Se a string não seguir o formato DD/MM/AAAA, se a data for
                    inválida (ex: 31/02) ou se for uma data futura.

    Exemplo:
        >>> calcular_idade('24/11/2006')
        19
    """
    nascimento_formatado = datetime.strptime(data_nascimento_str.strip(), '%d/%m/%Y')
    hoje = datetime.today()

    if nascimento_formatado > hoje:
        raise ValueError('A data de nascimento não pode estar no futuro.')

    # Verifica se já completou aniversário neste ano (compara mês e dia)
    fez_aniversario = (hoje.month, hoje.day) >= (nascimento_formatado.month, nascimento_formatado.day)
    ajuste = 0 if fez_aniversario else 1

    return (hoje.year - nascimento_formatado.year) - ajuste


# ==============================================================================
# 2. VALIDAÇÃO E FORMATAÇÃO DE CPF
# ==============================================================================

def validar_cpf(cpf_str: str) -> Optional[str]:
    """
    Valida matematicamente os dois dígitos verificadores do CPF e retorna o número formatado.

    Como usar:
        Passe qualquer string representando o CPF (com ou sem pontuação). A função
        avalia a regra do módulo 11 da Receita Federal. Se for válido, devolve
        a string mascarada; se for falso ou tiver tamanho incorreto, devolve None.

    Args:
        cpf_str (str): Documento CPF com 11 dígitos, pontuado ou não
                       (ex: '12345678909' ou '123.456.789-09').

    Returns:
        Optional[str]: O CPF formatado no padrão 'XXX.XXX.XXX-XX' se for válido,
                       ou None caso o documento seja inválido.

    Exemplo:
        >>> validar_cpf('12345678909')  # se válido
        '123.456.789-09'
        >>> validar_cpf('11111111111')  # se inválido
        None
    """
    validador = CPF()
    entrada_limpa = cpf_str.strip()

    if validador.validate(entrada_limpa):
        return validador.mask(entrada_limpa)
    return None


# ==============================================================================
# 3. CONSULTA DE CEP VIA API PÚBLICA
# ==============================================================================

def consultar_cep(cep: str) -> Optional[Dict[str, str]]:
    """
    Consulta o webservice público ViaCEP e devolve um dicionário padronizado do endereço.

    Como usar:
        Recebe o CEP com ou sem traço. A função limpa caracteres não numéricos,
        verifica se possui 8 dígitos, consome a API e retorna os dados de rua,
        bairro, cidade e estado. Se o CEP for inexistente na base dos Correios,
        retorna None.

    Args:
        cep (str): CEP com 8 dígitos (ex: '24800-000' ou '24800000').

    Returns:
        Optional[Dict[str, str]]: Dicionário com chaves 'cep', 'rua', 'bairro',
                                  'cidade' e 'uf', ou None se não encontrado.

    Raises:
        ValueError: Se a entrada não contiver exatamente 8 dígitos numéricos.
        requests.RequestException: Em casos de falha de conexão ou timeout na requisição.

    Exemplo:
        >>> consultar_cep('01001-000')
        {
            'cep': '01001-000',
            'rua': 'Praça da Sé',
            'bairro': 'Sé',
            'cidade': 'São Paulo',
            'uf': 'SP'
        }
    """
    cep_limpo = ''.join(filter(str.isdigit, cep))

    if len(cep_limpo) != 8:
        raise ValueError('O CEP deve conter exatamente 8 dígitos numéricos.')

    url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    dados = response.json()

    if dados.get('erro'):
        return None

    return {
        'cep': f'{cep_limpo[:5]}-{cep_limpo[5:]}',
        'rua': (dados.get('logradouro') or '').strip(),
        'bairro': (dados.get('bairro') or '').strip(),
        'cidade': (dados.get('localidade') or '').strip(),
        'uf': (dados.get('uf') or '').strip(),
    }


# ==============================================================================
# 4. VALIDAÇÃO E PARSING DE TELEFONE (NACIONAL E INTERNACIONAL)
# ==============================================================================

def validar_telefone(numero_str: str, regiao_padrao: str = 'BR') -> Optional[Dict[str, str]]:
    """
    Analisa, valida a existência estrutural e formata números de telefone fixo ou móvel.

    Como usar:
        Utiliza a biblioteca oficial Google libphonenumber. Aceita números locais
        com DDD (ex: '21984709360') ou internacionais com DDI (ex: '+1 650 253 0000').
        Detecta automaticamente a localidade geográfica correspondente ao DDD.

    Args:
        numero_str (str): Sequência do telefone digitada.
        regiao_padrao (str): Código ISO de 2 letras do país base assumido quando o usuário
                             não digita o '+' com o DDI (padrão: 'BR').

    Returns:
        Optional[Dict[str, str]]: Dicionário com as versões 'telefone_internacional',
                                  'telefone_nacional' e 'origem' (geolocalização/estado),
                                  ou None se o número for inválido ou impossível.

    Exemplo:
        >>> validar_telefone('21984709360')
        {
            'telefone_internacional': '+55 21 98470-9360',
            'telefone_nacional': '(21) 98470-9360',
            'origem': 'Rio de Janeiro'
        }
    """
    try:
        numero = phonenumbers.parse(numero_str.strip(), regiao_padrao)
    except NumberParseException:
        return None

    if not phonenumbers.is_possible_number(numero) or not phonenumbers.is_valid_number(numero):
        return None

    return {
        'telefone_internacional': phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        'telefone_nacional': phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.NATIONAL),
        'origem': geocoder.description_for_number(numero, 'pt-br') or 'Localização não identificada',
    }


# ==============================================================================
# 5. VALIDAÇÃO DE CARTÕES DE CRÉDITO E DÉBITO
# ==============================================================================

def algoritmo_luhn(numero_apenas_digitos: str) -> bool:
    """
    Executa o Algoritmo de Luhn (# 10) para checar o dígito verificador de um cartão.

    Como usar:
        Função auxiliar matemática. Não precisa ser chamada diretamente pelo usuário
        final; é utilizada internamente pela função `validar_cartao`.

    Args:
        numero_apenas_digitos (str): String composta exclusivamente por números (sem traços/espaços).

    Returns:
        bool: True se o checksum matemático for válido; False caso contrário.
    """
    soma = 0
    inverter = False

    for digito in reversed(numero_apenas_digitos):
        d = int(digito)
        if inverter:
            d *= 2
            if d > 9:
                d -= 9
        soma += d
        inverter = not inverter

    return soma % 10 == 0


def identificar_bandeira(numero_apenas_digitos: str) -> str:
    """
    Identifica a emissora/bandeira do cartão através de expressões regulares no BIN.

    Como usar:
        Avalia o prefixo e o padrão numérico do cartão. Suporta bandeiras comuns
        no Brasil e no exterior: Elo, Hipercard, Visa, Mastercard, American Express,
        Diners Club e Discover.

    Args:
        numero_apenas_digitos (str): Sequência limpa de números do cartão.

    Returns:
        str: Nome da bandeira identificada ou 'Desconhecida / Não mapeada'.
    """
    padroes = {
        'Elo': r'^(4011(78|79)|43(1274|8935)|45(1416|7393|763(1|2))|50(4175|6699|67[0-7][0-9]|9000)|627780|63(6297|6368)|650(03([^0])|04([0-9])|05(0|1)|4(0[5-9]|1[0-9]|2[0-9]|3[0-9])|4([4-9][0-9])|5([0-9][0-9])|9([0-9][0-9]))|6516(5[2-9]|[6-7][0-9])|6550([0-1][0-9]|2[1-9]|[3-4][0-9]|5[0-8]))',
        'Hipercard': r'^(606282\d{10}(\d{3})?)|(3841(00|40|60)\d{13})$',
        'Visa': r'^4[0-9]{12}(?:[0-9]{3})?$',
        'Mastercard': r'^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$',
        'American Express': r'^3[47][0-9]{13}$',
        'Diners Club': r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',
        'Discover': r'^6(?:011|5[0-9]{2})[0-9]{12}$',
    }

    for bandeira, regex in padroes.items():
        if re.match(regex, numero_apenas_digitos):
            return bandeira
    return 'Desconhecida / Não mapeada'


def validar_cartao(numero_cartao: str) -> Optional[Dict[str, str]]:
    """
    Realiza o pipeline completo de validação estrutural de um cartão bancário.

    Como usar:
        Recebe o número do cartão com ou sem pontuação/espaçamento. A função:
        1. Remove qualquer caractere que não seja número.
        2. Verifica se o comprimento está na faixa válida (13 a 19 dígitos).
        3. Valida os dígitos verificadores pelo Algoritmo de Luhn.
        4. Identifica a bandeira.
        5. Gera a máscara segura ocultando os dígitos centrais.

    Args:
        numero_cartao (str): Número do cartão (ex: '4532 0150 1234 5678').

    Returns:
        Optional[Dict[str, str]]: Dicionário com 'bandeira' e 'numero_mascarado',
                                  ou None se o cartão for inválido.

    Exemplo:
        >>> validar_cartao('4011 7800 1234 5678')
        {
            'bandeira': 'Elo',
            'numero_mascarado': '**** **** **** 5678'
        }
    """
    numero_limpo = re.sub(r'\D', '', numero_cartao)

    if not numero_limpo or len(numero_limpo) < 13 or len(numero_limpo) > 19:
        return None

    if not algoritmo_luhn(numero_limpo):
        return None

    return {
        'bandeira': identificar_bandeira(numero_limpo),
        'numero_mascarado': f'**** **** **** {numero_limpo[-4:]}',
    }