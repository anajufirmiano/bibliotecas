"""
Pacote de bibliotecas de validação e coleta de dados.
"""

from .funcoes.funcaoregra import (
    calcular_idade,
    validar_cpf,
    consultar_cep,
    validar_telefone,
    validar_cartao,
    algoritmo_luhn,
    identificar_bandeira,
)
from .funcoes.funcaocoleta import (
    lin,
    exibir_cabecalho,
    pedir_sexo,
    pedir_estado_civil,
    pedir_data_nascimento,
    pedir_cpf,
    pedir_endereco,
    pedir_telefone,
    pedir_cartao,
    exibir_menu_navegacao,
)

__all__ = [
    'calcular_idade',
    'validar_cpf',
    'consultar_cep',
    'validar_telefone',
    'validar_cartao',
    'algoritmo_luhn',
    'identificar_bandeira',
    'lin',
    'exibir_cabecalho',
    'pedir_sexo',
    'pedir_estado_civil',
    'pedir_data_nascimento',
    'pedir_cpf',
    'pedir_endereco',
    'pedir_telefone',
    'pedir_cartao',
    'exibir_menu_navegacao',
]
