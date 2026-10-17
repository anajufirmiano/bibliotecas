# 📦 Biblioteca de Validações e Coleta de Dados em Python

Uma biblioteca modular, didática e reutilizável desenvolvida em Python para **regras de negócio, validações cadastrais e interface de coleta interativa no terminal**.

O projeto adota uma arquitetura limpa com separação estrita de responsabilidades:
- **`funcaoregra.py`:** Regras de negócio e validações puras (sem dependência de terminal, sem `print()` ou `input()`), prontas para uso em APIs, backends e testes unitários.
- **`funcaocoleta.py`:** Camada de interface e experiência do usuário (CLI), com menus interativos, tratamento amigável de erros e loops de repetição.

---

## 🗂️ Estrutura do Módulo

```text
bibliotecas/
│
├── funcaoregra.py     # Lógica pura: cálculos, validações matemáticas e chamadas de API
├── funcaocoleta.py    # Interface: menus no terminal, captura de inputs e exibição
└── README.md          # Documentação completa da biblioteca
```

---

## 🚀 Funcionalidades

### 1. Regras de Negócio e Validações (`funcaoregra.py`)
| Função | Descrição | Retorno |
|---|---|---|
| `calcular_idade(data_str)` | Calcula a idade exata com base no dia e mês atual em relação a hoje. | `int` (idade em anos) |
| `validar_cpf(cpf_str)` | Validação matemática oficial dos dígitos verificadores (módulo 11). | `str` formatada (`XXX.XXX.XXX-XX`) ou `None` |
| `consultar_cep(cep_str)` | Consulta a API pública do ViaCEP e recupera rua, bairro, cidade e UF. | `dict` com dados do endereço ou `None` |
| `validar_telefone(numero_str)` | Validação estrutural de telefones móveis/fixos com geolocalização. | `dict` com formato nacional, internacional e região |
| `algoritmo_luhn(numero)` | Implementação do algoritmo de Luhn (módulo 10) para verificação de cartões. | `bool` (`True`/`False`) |
| `identificar_bandeira(numero)` | Detecção de bandeiras (Visa, Mastercard, Elo, Hipercard, Amex, Diners, Discover). | `str` com o nome da bandeira |
| `validar_cartao(numero)` | Validação completa de cartão (Luhn + Bandeira + máscara de segurança). | `dict` com bandeira e máscara (`**** 1234`) |

### 2. Interface e Coleta de Dados (`funcaocoleta.py`)
| Função | O que faz no terminal |
|---|---|
| `lin(tamanho, caractere)` | Imprime linhas divisórias estilizadas no terminal. |
| `exibir_cabecalho(titulo)` | Exibe títulos centralizados e padronizados. |
| `pedir_sexo()` | Menu interativo com opções numéricas (`Feminino`/`Masculino`). |
| `pedir_estado_civil()` | Menu interativo para seleção de estado civil (`Solteiro`, `Casado`, etc.). |
| `pedir_nascimento()` | Loop de coleta de data com tratamento de formato e cálculo de idade. |
| `pedir_cpf()` | Coleta com validação de dígitos e opção de cancelamento (`'sair'`). |
| `pedir_endereco()` | Busca via CEP com preenchimento automático e coleta de número e complemento. |
| `pedir_telefone()` | Coleta e validação de telefones com DDD/DDI. |
| `pedir_cartao()` | Captura e validação segura de dados de cartão de crédito. |
| `exibir_menu_navegacao()` | Menu de navegação para continuidade ou saída de fluxos. |

---

## 🛠️ Instalação das Dependências

Para utilizar os recursos de validação de documentos, telefone e requisições HTTP, instale os pacotes necessários:

```bash
pip install requests validate-docbr phonenumbers
```

---

## 💻 Como Usar nos seus Projetos

### Exemplo 1: Utilizando apenas as validações puras (Ideal para Backend ou APIs)
```python
from bibliotecas.funcaoregra import calcular_idade, validar_cpf, consultar_cep

# Cálculo de idade exata
idade = calcular_idade('24/11/2006')
print(f'Idade: {idade} anos')

# Validação e máscara de CPF
cpf_formatado = validar_cpf('12345678909')
if cpf_formatado:
    print(f'CPF válido: {cpf_formatado}')
else:
    print('CPF inválido!')

# Consulta de CEP automática
endereco = consultar_cep('01001-000')
if endereco:
    print(f"Rua: {endereco['rua']}, {endereco['bairro']} - {endereco['cidade']}/{endereco['uf']}")
```

### Exemplo 2: Utilizando a camada de coleta interativa (Ideal para CLI / Terminal)
```python
from bibliotecas.funcaocoleta import (
    exibir_cabecalho,
    pedir_sexo,
    pedir_cpf,
    pedir_endereco,
    pedir_telefone
)

exibir_cabecalho("NOVO CADASTRO DE CLIENTE")

sexo = pedir_sexo()
cpf = pedir_cpf()
telefone = pedir_telefone()
endereco = pedir_endereco()

print("\nCadastro concluído com sucesso!")
```

---

## 🎯 Vantagens da Modularização

1. **Reutilização de Código:** As mesmas funções podem ser aproveitadas em múltiplos projetos (como sistemas bancários, cadastros de academias, e-commerces, etc.).
2. **Separação de Preocupações:** Quem calcula não se preocupa com `input()`, e quem coleta não precisa reimplementar validações complexas.
3. **Facilidade de Testes:** Funções puras podem ser testadas unitariamente de forma automatizada sem travar esperando entrada de usuário.
4. **Tratamento de Exceções Seguro:** Acesso a APIs com proteção de timeout e tratamento de erros de rede.

---

## 👩‍💻 Autora

Desenvolvido por **[Ana Júlia Firmiano](https://github.com/anajufirmiano)**.
