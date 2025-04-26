import random
import time
import os
import sys
from collections import defaultdict
from datetime import datetime


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


commands = [
    # Navegação (40% básico, 30% médio, 30% difícil)
    {
        "desc": "Mover para esquerda",
        "respostas": ["h"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Mover para baixo",
        "respostas": ["j"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Mover para cima",
        "respostas": ["k"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Mover para direita",
        "respostas": ["l"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Início da próxima palavra",
        "respostas": ["w"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Final da palavra",
        "respostas": ["e"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Início da linha",
        "respostas": ["0", "^"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Final da linha",
        "respostas": ["$"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Início do arquivo",
        "respostas": ["gg"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Final do arquivo",
        "respostas": ["G"],
        "cat": "navegação",
        "dificuldade": 1,
    },
    {
        "desc": "Linha específica (42)",
        "respostas": ["42G", ":42"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Centralizar linha atual na tela",
        "respostas": ["zz"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Mover para o topo da tela",
        "respostas": ["H"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Mover para o meio da tela",
        "respostas": ["M"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Mover para o final da tela",
        "respostas": ["L"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Navegar para definição",
        "respostas": ["gd"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Navegar entre parágrafos",
        "respostas": ["}", "{"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Mover para o início de uma seção",
        "respostas": ["[["],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Mover para o fim de uma seção",
        "respostas": ["]]"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Saltar para a próxima ocorrência de um caractere",
        "respostas": ["f"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Navegar entre buffers",
        "respostas": [":bn", ":bp"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Navegar para a última posição",
        "respostas": ["''", "``"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Busca de função",
        "respostas": ["[[", "]]"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Navegar para o próximo método",
        "respostas": ["]m"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Navegar para o método anterior",
        "respostas": ["[m"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Navegar entre janelas divididas",
        "respostas": ["Ctrl+w w", "Ctrl+w h/j/k/l"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    {
        "desc": "Rolar uma página para baixo",
        "respostas": ["Ctrl+f"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Rolar uma página para cima",
        "respostas": ["Ctrl+b"],
        "cat": "navegação",
        "dificuldade": 2,
    },
    {
        "desc": "Usar marcas para navegação",
        "respostas": ["ma", "'a"],
        "cat": "navegação",
        "dificuldade": 3,
    },
    # Edição (30% básico, 40% médio, 30% difícil)
    {
        "desc": "Entrar no modo inserção",
        "respostas": ["i"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo inserção após o cursor",
        "respostas": ["a"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo inserção no início da linha",
        "respostas": ["I"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo inserção no final da linha",
        "respostas": ["A"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo inserção na linha abaixo",
        "respostas": ["o"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo inserção na linha acima",
        "respostas": ["O"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {"desc": "Deletar linha", "respostas": ["dd"], "cat": "edição", "dificuldade": 1},
    {
        "desc": "Copiar linha",
        "respostas": ["yy", "Y"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Colar após o cursor",
        "respostas": ["p"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Colar antes do cursor",
        "respostas": ["P"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Desfazer última alteração",
        "respostas": ["u"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Refazer alteração desfeita",
        "respostas": ["Ctrl+r"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Substituir caractere sob o cursor",
        "respostas": ["r"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Deletar caractere sob o cursor",
        "respostas": ["x"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Deletar caractere antes do cursor",
        "respostas": ["X"],
        "cat": "edição",
        "dificuldade": 1,
    },
    {
        "desc": "Alterar uma palavra",
        "respostas": ["cw"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar até o final da linha",
        "respostas": ["c$", "C"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar entre aspas simples",
        "respostas": ["ci'"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar entre aspas duplas",
        "respostas": ['ci"'],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar entre parênteses",
        "respostas": ["ci(", "ci)"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar entre colchetes",
        "respostas": ["ci[", "ci]"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Alterar entre chaves",
        "respostas": ["ci{", "ci}"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Juntar linhas",
        "respostas": ["J"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Indentar linha",
        "respostas": [">>"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Remover indentação",
        "respostas": ["<<"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Deletar até o final da palavra",
        "respostas": ["dw"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Deletar até o final da linha",
        "respostas": ["d$", "D"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Deletar até o início da linha",
        "respostas": ["d0", "d^"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {"desc": "Formatar JSON", "respostas": ["=j"], "cat": "edição", "dificuldade": 3},
    {
        "desc": "Formatar todo o arquivo",
        "respostas": ["gg=G"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Mudar para maiúsculas",
        "respostas": ["gU"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Mudar para minúsculas",
        "respostas": ["gu"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Inverter maiúsculas/minúsculas",
        "respostas": ["~"],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Operar em várias linhas",
        "respostas": ["visual + command"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Macro de edição",
        "respostas": ["q"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Executar macro",
        "respostas": ["@"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Repetir última alteração",
        "respostas": ["."],
        "cat": "edição",
        "dificuldade": 2,
    },
    {
        "desc": "Substituir no escopo visual",
        "respostas": [":'<,'>s/old/new/g"],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Copiar para o registro 'a'",
        "respostas": ['"ayy'],
        "cat": "edição",
        "dificuldade": 3,
    },
    {
        "desc": "Colar do registro 'a'",
        "respostas": ['"ap'],
        "cat": "edição",
        "dificuldade": 3,
    },
    # Busca/Substituição (20% básico, 50% médio, 30% difícil)
    {
        "desc": "Buscar texto para frente",
        "respostas": ["/"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Buscar texto para trás",
        "respostas": ["?"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Próxima ocorrência",
        "respostas": ["n"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Ocorrência anterior",
        "respostas": ["N"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Buscar palavra atual",
        "respostas": ["*"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Buscar palavra atual para trás",
        "respostas": ["#"],
        "cat": "busca",
        "dificuldade": 1,
    },
    {
        "desc": "Substituir em todo o arquivo",
        "respostas": [":%s/old/new/g"],
        "cat": "busca",
        "dificuldade": 2,
    },
    {
        "desc": "Substituir com confirmação",
        "respostas": [":%s/old/new/gc"],
        "cat": "busca",
        "dificuldade": 2,
    },
    {
        "desc": "Substituir na linha atual",
        "respostas": [":s/old/new/g"],
        "cat": "busca",
        "dificuldade": 2,
    },
    {
        "desc": "Substituir na seleção visual",
        "respostas": [":'<,'>s/old/new/g"],
        "cat": "busca",
        "dificuldade": 2,
    },
    {
        "desc": "Limpar highlights",
        "respostas": [":noh"],
        "cat": "busca",
        "dificuldade": 2,
    },
    {
        "desc": "Buscar nas próximas 5 linhas",
        "respostas": ["/pattern/;+5"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Substituir com regex",
        "respostas": [":%s/\\vpattern/replace/g"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Buscar padrão no início da linha",
        "respostas": ["/^pattern"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Buscar padrão no final da linha",
        "respostas": ["/pattern$"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Buscar qualquer dígito",
        "respostas": ["/\\d"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Buscar qualquer não-dígito",
        "respostas": ["/\\D"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Buscar qualquer caractere alfanumérico",
        "respostas": ["/\\w"],
        "cat": "busca",
        "dificuldade": 3,
    },
    {
        "desc": "Listar todas as ocorrências de um padrão",
        "respostas": [":g/pattern"],
        "cat": "busca",
        "dificuldade": 3,
    },
    # Visual/Seleção (nova categoria)
    {
        "desc": "Entrar no modo visual",
        "respostas": ["v"],
        "cat": "visual",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo visual de linha",
        "respostas": ["V"],
        "cat": "visual",
        "dificuldade": 1,
    },
    {
        "desc": "Entrar no modo visual de bloco",
        "respostas": ["Ctrl+v"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar palavra inteira",
        "respostas": ["viw"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar entre aspas",
        "respostas": ['vi"', "vi'"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar entre parênteses",
        "respostas": ["vi(", "vi)"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar entre chaves",
        "respostas": ["vi{", "vi}"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar entre colchetes",
        "respostas": ["vi[", "vi]"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar parágrafo",
        "respostas": ["vip"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar até o final do arquivo",
        "respostas": ["vG"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Selecionar até o início do arquivo",
        "respostas": ["vgg"],
        "cat": "visual",
        "dificuldade": 2,
    },
    {
        "desc": "Reselecionar última seleção visual",
        "respostas": ["gv"],
        "cat": "visual",
        "dificuldade": 3,
    },
    {
        "desc": "Editar múltiplas linhas com mesmo prefixo",
        "respostas": ["Ctrl+v + I"],
        "cat": "visual",
        "dificuldade": 3,
    },
    {
        "desc": "Editar múltiplas linhas com mesmo sufixo",
        "respostas": ["Ctrl+v + A"],
        "cat": "visual",
        "dificuldade": 3,
    },
    # Configurações/Comandos (nova categoria)
    {
        "desc": "Salvar arquivo",
        "respostas": [":w"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Sair",
        "respostas": [":q"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Salvar e sair",
        "respostas": [":wq", "ZZ"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Sair sem salvar",
        "respostas": [":q!"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Salvar como",
        "respostas": [":w nome_arquivo"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Abrir arquivo",
        "respostas": [":e nome_arquivo"],
        "cat": "comandos",
        "dificuldade": 1,
    },
    {
        "desc": "Dividir janela horizontalmente",
        "respostas": [":sp", ":split"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Dividir janela verticalmente",
        "respostas": [":vsp", ":vsplit"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Mostrar números de linha",
        "respostas": [":set number", ":set nu"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Ocultar números de linha",
        "respostas": [":set nonumber", ":set nonu"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Mostrar espaços em branco",
        "respostas": [":set list"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Ativar destaque de sintaxe",
        "respostas": [":syntax on"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Abrir nova aba",
        "respostas": [":tabnew"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Navegar para próxima aba",
        "respostas": [":tabn", "gt"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Navegar para aba anterior",
        "respostas": [":tabp", "gT"],
        "cat": "comandos",
        "dificuldade": 2,
    },
    {
        "desc": "Executar comando shell",
        "respostas": [":!comando"],
        "cat": "comandos",
        "dificuldade": 3,
    },
    {
        "desc": "Definir mapeamento de tecla",
        "respostas": [":map"],
        "cat": "comandos",
        "dificuldade": 3,
    },
    {
        "desc": "Recarregar arquivo",
        "respostas": [":e!"],
        "cat": "comandos",
        "dificuldade": 3,
    },
    {
        "desc": "Ativar modo de diferença",
        "respostas": [":diffthis"],
        "cat": "comandos",
        "dificuldade": 3,
    },
    {
        "desc": "Próximo ponto de diferença",
        "respostas": ["]c"],
        "cat": "comandos",
        "dificuldade": 3,
    },
]

# Dicas expandidas para ajudar o aprendizado
dicas = {
    "h": "Tecla à esquerda do 'j' no teclado QWERTY - pense em 'esquerda'",
    "j": "Seta para baixo - lembre da posição no teclado (parece uma seta para baixo)",
    "k": "Seta para cima - acima do 'j' no teclado QWERTY",
    "l": "Tecla à direita do 'k' no teclado - pense em 'direita'",
    "w": "Vem de 'word' - avança para o início da próxima palavra",
    "e": "Vem de 'end' - vai para o final da palavra atual",
    "b": "Vem de 'back' - volta para o início da palavra atual",
    "gg": "Dois 'g's levam ao início (top) do arquivo",
    "G": "G maiúsculo leva ao final (bottom) do arquivo",
    "0": "Número zero - vai para a coluna zero (início absoluto da linha)",
    "^": "Circunflexo - vai para o primeiro caractere não-branco da linha",
    "$": "Cifrão - lembra o 'final' como em 'fim de linha' em expressões regulares",
    "i": "Vem de 'insert' - insere antes do cursor",
    "a": "Vem de 'append' - insere após o cursor",
    "o": "Cria uma nova linha abaixo e entra no modo inserção",
    "O": "Cria uma nova linha acima e entra no modo inserção",
    "dd": "Delete uma linha inteira - d duas vezes",
    "yy": "Yank (copiar) uma linha inteira - y duas vezes",
    "p": "Paste (colar) após o cursor",
    "P": "Paste (colar) antes do cursor",
    "u": "Undo - desfaz última alteração",
    "Ctrl+r": "Redo - refaz alterações desfeitas",
    "/": "Inicia busca para frente (forward)",
    "?": "Inicia busca para trás (backward)",
    "n": "Next - próxima ocorrência na mesma direção",
    "N": "Next na direção oposta",
    "*": "Busca a palavra sob o cursor para frente",
    "#": "Busca a palavra sob o cursor para trás",
    ":%s/old/new/g": "Substitui 'old' por 'new' em todo o arquivo (g = global)",
    ":%s/old/new/gc": "Substitui com confirmação (c = confirm/check)",
    "v": "Modo Visual - seleciona caracteres",
    "V": "Modo Visual Line - seleciona linhas inteiras",
    "Ctrl+v": "Visual Block - seleciona blocos retangulares",
    ":w": "Write - salva o arquivo",
    ":q": "Quit - sai do Vim",
    ":wq": "Write and Quit - salva e sai",
    "ZZ": "Atalho para :wq - salva e sai",
    ":q!": "Força a saída sem salvar",
    "ci'": "'Change inside quotes' - altera conteúdo entre aspas simples",
    'ci"': "'Change inside double quotes' - altera conteúdo entre aspas duplas",
    "ci(": "'Change inside parentheses' - altera conteúdo entre parênteses",
    "ci{": "'Change inside braces' - altera conteúdo entre chaves",
    "=j": "Formata JSON usando o comando de igualdade + movimento",
    "q": "Grava macros - use q seguido de uma letra para registrar",
    "[[": "Navega entre funções em muitas linguagens de programação",
    ":noh": "No highlight - desativa o destaque de busca",
    "J": "Join - une a linha atual com a linha abaixo",
    ">>": "Indenta a linha atual para a direita",
    "<<": "Remove indentação da linha atual",
    "~": "Inverte maiúsculas/minúsculas do caractere sob o cursor",
    ".": "Repete o último comando - muito útil!",
    "f": "Find - encontra um caractere na linha atual",
    "t": "Till - move até antes de um caractere na linha atual",
    ";": "Repete o último f, F, t, ou T",
    ",": "Repete o último f, F, t, ou T na direção oposta",
    "zz": "Centraliza a linha atual na tela",
    "zt": "Coloca a linha atual no topo da tela",
    "zb": "Coloca a linha atual no final da tela",
    "H": "'High' - move para o topo da tela",
    "M": "'Middle' - move para o meio da tela",
    "L": "'Low' - move para o final da tela",
    ":sp": "'Split' - divide a janela horizontalmente",
    ":vsp": "'Vertical split' - divide a janela verticalmente",
    "Ctrl+w w": "Alterna entre janelas divididas",
}


def menu_categorias():
    cats = list(set(cmd["cat"] for cmd in commands))
    print("\n📚 Categorias Disponíveis:")
    for i, cat in enumerate(sorted(cats), 1):
        print(f"{i}. {cat.capitalize()}")
    selecao = input("\nEscolha categorias (ex: 1,3): ").strip()
    return [sorted(cats)[int(i) - 1] for i in selecao.split(",") if i.isdigit()]


def menu_dificuldade():
    print("\n🎚 Níveis de Dificuldade:")
    print("1. Fácil (Fundamentos)")
    print("2. Médio (Técnicas Intermediárias)")
    print("3. Difícil (Fluxos Complexos)")
    return int(input("Escolha o nível (1-3): ").strip())


def selecionar_questoes(categorias, nivel):
    """Seleção balanceada com curva de aprendizado"""
    peso_dificuldade = {
        1: [0.8, 0.2, 0.0],  # 80% básico, 20% médio
        2: [0.3, 0.5, 0.2],  # 30% básico, 50% médio, 20% difícil
        3: [0.1, 0.3, 0.6],  # 10% básico, 30% médio, 60% difícil
    }

    quests = []
    for cmd in commands:
        if cmd["cat"] in categorias:
            for diff, prob in enumerate(peso_dificuldade[nivel], start=1):
                if cmd["dificuldade"] == diff and random.random() < prob:
                    quests.append(cmd)
                    break
    return random.sample(quests, min(15, len(quests)))


def quiz():
    print("\n🎯 Modo Quiz - Escolha seu desafio!")
    cats = menu_categorias()
    nivel = menu_dificuldade()

    questoes = selecionar_questoes(cats, nivel)
    if not questoes:
        print("Nenhuma questão encontrada com esses filtros!")
        return

    random.shuffle(questoes)
    acertos = 0
    start = time.time()

    for i, cmd in enumerate(questoes, 1):
        print(f"\n📌 Questão {i}/{len(questoes)}")
        print(f"🔧 Categoria: {cmd['cat'].capitalize()}")
        print(f"🏷️  Ação: {cmd['desc']}")

        resp = input("⌨️  Comando: ").strip()
        if resp in cmd["respostas"]:
            print("✅ Correto!")
            acertos += 1
        else:
            print(f"❌ Errado! Resposta(s): {', '.join(cmd['respostas'])}")
            print(
                f"💡 Dica: {dicas.get(cmd['respostas'][0], 'Pratique mais este comando!')}"
            )

        if i % 5 == 0:
            print(f"\n⭐ Progresso: {acertos}/{i} acertos")

    print(f"\n🎉 Resultado Final: {acertos}/{len(questoes)}")
    print(f"⏱️  Tempo: {time.time()-start:.1f}s")

    # Relatório detalhado
    print("\n📊 Desempenho por Categoria:")
    categorias_report = defaultdict(int)
    for cmd in questoes:
        categorias_report[cmd["cat"]] += 1
    for cat, total in categorias_report.items():
        acertos_cat = sum(
            1 for c in questoes if c["cat"] == cat and c["respostas"][0] in dicas
        )
        print(f"- {cat.capitalize()}: {acertos_cat}/{total}")


def gerar_exercicio_pratico():
    """
    Gera arquivos de exercícios práticos para treinamento de Vim,
    organizados por categorias e níveis de dificuldade.
    Cada arquivo contém no máximo 4 exercícios com explicações claras.
    """
    exercicios = [
        # NAVEGAÇÃO BÁSICA
        {
            "arquivo": "01-navegacao-basica.md",
            "conteudo": """# 🧭 Navegação Básica no Vim

## 🎯 Objetivos de Aprendizado
- Dominar movimentos básicos (h, j, k, l) e saltos simples (w, b, 0, $)
- Navegar por palavras e linhas com eficiência
- Pular para posições específicas no arquivo


## 📝 Exercício 1: Movimentos Fundamentais

```python
def hello_world():
    # Use h, j, k, l para navegar 
    # até estas linhas de comentários
    print("Hello")
    print("Vim")
    print("World")
    # O objetivo é se movimentar
    # sem usar as setas direcionais
    return True
```

### Tarefas:
1. [ ] Navegue até a linha com `print("Hello")` usando `j`
2. [ ] Mova para a palavra `Vim` usando movimentos `j` e `l`
3. [ ] Volte para o início da palavra `def` usando `k` repetidamente
4. [ ] Mova para o final da linha `return True` usando `$`
5. [ ] Vá para o início da linha atual com `0`

## 📝 Exercício 2: Navegação por Palavras

```
const usuarios = [
  { id: 1, nome: "Ana", idade: 28, cidade: "São Paulo" },
  { id: 2, nome: "Bruno", idade: 34, cidade: "Rio de Janeiro" },
  { id: 3, nome: "Carla", idade: 22, cidade: "Belo Horizonte" }
];

function encontrarUsuario(id) {
  return usuarios.find(user => user.id === id);
}
```

### Tarefas:
1. [ ] Navegue até a palavra `nome` na primeira linha usando `w` (word)
2. [ ] Pule para o próximo `id` usando `w` repetidamente
3. [ ] Vá para o final da palavra `idade` usando `e` (end)
4. [ ] Volte para o início de `cidade` usando `b` (back)
5. [ ] Pule para a função `encontrarUsuario` com `}` (próximo bloco)

## Exercício 3: Navegação Vertical
```
Linha 1 - Use 'j' para descer até aqui
Linha 2
Linha 3
Linha 4
Linha 5 - Use '59G' para saltar diretamente para esta linha (linha 37 como digitado)
Linha 6
Linha 7
Linha 8 - Use 'gg' para voltar ao topo do arquivo e depois '62G' para vir aqui
Fim
```

### Tarefas:
1. [ ] Vá para o início do arquivo com `gg`
2. [ ] Pule para a linha 10 usando `59G`
3. [ ] Vá para o final do arquivo com `G`
4. [ ] Vá para a linha final usando `/Fim` e Enter
5. [ ] Centralize a tela na linha atual usando `zz`

## Exercício 4: Precisão em Blocos
```javascript
const pessoa = {
    nome: "Ana", // Use 'f,' para saltar até a vírgula
    idade: 28,   // Use 'tx' para ir antes do 'x' em qualquer posição
    cidade: "Porto" // Use '$' para ir ao final da linha
};
```
## 💡 Dicas de Navegação
- `h`, `j`, `k`, `l` substituem as setas direcionais
- `w` (word) pula para o início da próxima palavra
- `e` (end) vai para o final da palavra atual/próxima
- `b` (back) volta para o início da palavra anterior
- `0` vai para o início da linha
- `$` vai para o fim da linha
- `gg` vai para o topo do arquivo
- `G` vai para o final do arquivo
- `{número}G` vai para a linha específica
- `zz` centraliza a linha atual na tela

## 🚀 Desafio Bônus
Tente navegar pelo arquivo inteiro usando apenas comandos Vim, sem tocar no mouse ou nas setas do teclado por 5 minutos!

> **Dica:** Pratique estes movimentos até que se tornem automáticos. A eficiência no Vim começa com a navegação fluida!
""",
        },
        # EDIÇÃO BÁSICA
        {
            "arquivo": "02-edicao-basica.md",
            "conteudo": """# ✏️ Edição Básica no Vim

## 🎯 Objetivos de Aprendizado
- Dominar comandos de inserção de texto
- Aprender a deletar, copiar e colar eficientemente
- Utilizar comandos compostos para edições rápidas

## 📝 Exercício 0: Modos de Inserção
```
Posicione o cursor aqui e experimente diferentes formas de entrar no modo de inserção:
- 'i' para inserir antes do cursor
- 'a' para inserir depois do cursor
- 'I' para inserir no início da linha
- 'A' para inserir no final da linha
- 'o' para criar uma nova linha abaixo
- 'O' para criar uma nova linha acima
```

## 📝 Exercício 1: Inserção de Texto

```python
def calcular_media():
    notas = [7.5, 8.0, 6.5]
    # Insira uma linha aqui que soma as notas
    # Insira uma linha aqui que calcula a média
    return media
```

### Tarefas:
1. [ ] Posicione o cursor depois de `notas = [7.5, 8.0, 6.5]` 
2. [ ] Pressione `o` para inserir uma nova linha abaixo
3. [ ] Digite `soma = sum(notas)`
4. [ ] Pressione `o` novamente para criar outra linha
5. [ ] Digite `media = soma / len(notas)`
6. [ ] Pressione `ESC` para voltar ao modo normal
7. [ ] Use `O` (maiúsculo) para inserir uma linha acima de `return media`
8. [ ] Digite `print(f"A média é {media}")`


## 📝 Exercício 2: Deleção e Substituição

```python
def limpar_texto():
    # Delete esta linha inteira com 'dd'
    mensagem = "Esta parte deve ser deletada com 'dw'"
    # Use 'D' para deletar do cursor até o final da linha: isto deve permanecer
    codigo = 12345  # Delete apenas o número com 'd5l'
```


```javascript
function processarDados(dados) {
  const resultados = [];
  
  // Este comentário deve ser removido
  // Este comentário também
  
  for (let i = 0; i < dados.length; i++) {
    const item = dados[i];
    const valor = item.valor * 2; // Multiplicar por 3 ao invés de 2
    resultados.push(valor);
  }
  
  return resultados.filter(valor => valor > 0);
}
```

### Tarefas:
1. [ ] Delete a linha `// Este comentário deve ser removido` usando `dd`
2. [ ] Delete a próxima linha de comentário da mesma forma
3. [ ] Vá até `* 2` no comentário e use `r` para substituir `2` por `3`
4. [ ] Use `cw` (change word) para substituir `valor` por `resultado` na linha que declara a constante
5. [ ] Use `C` (change to end) na linha `const item = dados[i];` e complete com `elemento = dados[i].processado;`



## Exercício 3: Copiar e Colar
```
1. Copie esta linha inteira com 'yy'
2. Mova o cursor para a linha abaixo
3. Cole a linha copiada com 'p'
4. Use 'yaw' para copiar uma palavra inteira (with surrounding space)
5. Cole a palavra em outro lugar

ÁREA DE TESTE PARA COLAR:

```

```html
<div class="card">
  <h2>Título do Card</h2>
  <p>Descrição do card aqui.</p>
  <button>Clique aqui</button>
</div>

<!-- Crie mais dois cards aqui -->
```

### Tarefas:
1. [ ] Selecione todas as linhas do primeiro card com `V` (visual line) e movimentos
2. [ ] Copie a seleção com `y` (yank)
3. [ ] Mova o cursor para depois do comentário
4. [ ] Cole o conteúdo duas vezes com `p`
5. [ ] No segundo card copiado, use `cit` dentro da tag `<h2>` para mudar para "Segundo Card"
6. [ ] No terceiro card, use `cit` dentro da tag `<h2>` para mudar para "Terceiro Card"

## 📝 Exercício 4: Desfazer e Refazer

```css
body {
  font-family: Arial;
  color: #333333;
  background-color: white;
  margin: 0;
  padding: 20px;
}
```

### Tarefas:
1. [ ] Mude `Arial` para `"Helvetica, Arial, sans-serif"` usando `ci'` (change inside quotes)
2. [ ] Desfaça a alteração usando `u`
3. [ ] Refaça a alteração usando `Ctrl+r`
4. [ ] Altere `#333333` para `#444444` com `ct3` (change till 3) e digite `444444`
5. [ ] Altere `white` para `#f5f5f5` usando `cw`

## 💡 Dicas de Edição
- `i` entra no modo de inserção no local atual
- `a` entra no modo de inserção após o caractere atual
- `o` abre uma nova linha abaixo e entra no modo de inserção
- `O` abre uma nova linha acima e entra no modo de inserção
- `dd` deleta a linha atual
- `yy` copia a linha atual
- `p` cola após o cursor
- `P` cola antes do cursor
- `r` substitui um único caractere
- `cw` muda a palavra atual
- `C` muda do cursor até o final da linha
- `u` desfaz a última alteração
- `Ctrl+r` refaz a última alteração desfeita

## 🚀 Desafio Bônus
Crie uma função completa que calcule o fatorial de um número, usando apenas comandos Vim para escrever o código (sem copy/paste externo).

> **Dica:** A edição eficiente no Vim combina operadores (d, c, y) com movimentos (w, $, etc.). Dominar esta combinação é a chave para trabalhar rapidamente!""",
        },
        # BUSCA & SUBSTITUIÇÃO
        {
            "arquivo": "03-busca-substituicao.md",
            "conteudo": """ # 🔍 Busca e Substituição no Vim
## 🎯 Objetivos de Aprendizado
- Dominar comandos de busca eficientes
- Aprender padrões de substituição
- Usar expressões regulares para edições avançadas

## 📝 Exercício 1: Busca Básica

```python
def processar_dados(lista):
    resultado = []
    for item in lista:
        if item > 10:
            resultado.append(item * 2)
        elif item > 5:
            resultado.append(item + 5)
        else:
            resultado.append(item)
    return resultado

# Outras funções abaixo
def filtrar_dados(lista):
    return [item for item in lista if item % 2 == 0]

def ordenar_dados(lista):
    return sorted(lista)
```

### Tarefas:
1. [ ] Busque pela palavra `resultado` usando `/resultado` e Enter
2. [ ] Encontre a próxima ocorrência com `n`
3. [ ] Encontre a ocorrência anterior com `N`
4. [ ] Busque pela palavra "lista" usando `*` quando o cursor estiver sobre ela
5. [ ] Limpe o destaque da busca com `:noh`

## Exercício 2: Busca Instantânea com '*'
```python
def processar_dados(entrada):
    # Posicione o cursor sobre a palavra 'entrada' e pressione '*'
    # Observe como o Vim destaca todas as ocorrências de 'entrada'
    resultado = transformar(entrada)
    if validar(entrada):
        return resultado
    else:
        return entrada
```

## Exercício 3: Substituição Simples
```
Neste exercício, você vai substituir palavras:

1. Substitua 'gato' por 'cão' na linha abaixo:
   O gato preto caçava o gato cinza enquanto outro gato dormia.

2. Use a sintaxe ':%s/palavra-velha/palavra-nova/g' para substituir em todo o arquivo
   Substitua todas as ocorrências de 'palavra' por 'termo'
   
palavra palavra palavra palavra
```

## 📝 Exercício 4: Substituição em Linhas
```
const config = {
  apiUrl: 'http://api.exemplo.com',
  timeout: 1000,
  retryCount: 3,
  debug: false,
  apiKey: 'abc123'
};

fetch(config.apiUrl)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### Tarefas:
1. [ ] Mude todas as ocorrências de `api` para `service` na linha de `apiUrl` usando `:s/api/service/g`
2. [ ] Substitua `http://` por `https://` usando `:s/http:/https:/`
3. [ ] Mude o valor de `timeout` de `1000` para `2000` usando `:s/timeout: 1000/timeout: 2000/`
4. [ ] Altere `debug: false` para `debug: true` usando `:s/false/true/`
5. [ ] Substitua o valor de `apiKey` por `xyz789` usando `:s/'abc123'/'xyz789'/`


## 📝 Exercício 4: Substituição Global

```html
<div class="container">
  <div class="item">Item 1</div>
  <div class="item">Item 2</div>
  <div class="item">Item 3</div>
  <div class="item">Item 4</div>
  <div class="item">Item 5</div>
</div>
```

### Tarefas:
1. [ ] Substitua todas as ocorrências de `class="item"` por `class="box"` usando `:%s/class="item"/class="box"/g`
2. [ ] Adicione um atributo `data-id` a cada box, numerado sequencialmente, usando `:%s/<div class="box">/<div class="box" data-id="item-&">/g`
3. [ ] Mude todos os "Item" para "Produto" usando `:%s/Item/Produto/g`
4. [ ] Adicione um ponto de exclamação após cada número usando `:%s/\(\d\)$/\1!/g`

## Exercício 5: Substituição com Confirmação
```css
.header {
  background-color: blue;
  color: white;
}

.footer {
  background-color: blue;
  color: white;
}

.sidebar {
  background-color: blue;
  color: white;
}

.content {
  background-color: white;
  color: black;
}
```

### Tarefas:
1. [ ] Substitua `blue` por `#336699` com confirmação para cada ocorrência usando `:%s/blue/#336699/gc`
2. [ ] Confirme a substituição para `.header` e `.footer`, mas não para `.sidebar`
3. [ ] Substitua `white` por `#f8f8f8` apenas nas classes `.header` e `.footer` usando busca com intervalo de linhas
4. [ ] Altere todos os valores de cor para formato rgb usando expressões regulares

## 📝 Exercício 6: Substituição Avançada com Regex

```
Nome: João Silva, Idade: 32, Email: joao.silva@email.com
Nome: Maria Souza, Idade: 28, Email: maria_souza@email.com
Nome: Pedro Santos, Idade: 45, Email: pedro-santos@email.com
Nome: Ana Oliveira, Idade: 36, Email: ana.oliveira@email.com
```

### Tarefas:
1. [ ] Formate os emails para ficarem entre <> usando `:%s/@\([^,]*\)/@<\1>/g`
2. [ ] Adicione o título "Sr." antes dos nomes masculinos e "Sra." antes dos femininos
3. [ ] Reordene cada linha para o formato "Email / Nome / Idade" usando grupos de captura
4. [ ] Destaque as idades acima de 30 colocando-as entre asteriscos

## 💡 Dicas de Busca e Substituição
- `/palavra` busca a palavra para frente
- `?palavra` busca a palavra para trás
- `*` busca a palavra sob o cursor para frente
- `#` busca a palavra sob o cursor para trás
- `n` vai para a próxima ocorrência
- `N` vai para a ocorrência anterior
- `:s/antigo/novo/` substitui a primeira ocorrência na linha
- `:s/antigo/novo/g` substitui todas as ocorrências na linha
- `:%s/antigo/novo/g` substitui em todo o arquivo
- `:%s/antigo/novo/gc` substitui em todo o arquivo com confirmação
- `:noh` limpa o destaque da busca

## 🚀 Desafio Bônus
Dado um arquivo com uma lista de emails não formatados, use substituição com expressões regulares para transformá-los em links HTML `<a href="mailto:email@dominio.com">email@dominio.com</a>`.

> **Dica:** A busca e substituição são extremamente poderosas no Vim, especialmente quando combinadas com expressões regulares para padrões complexos!
""",
        },
        # COMANDOS AVANÇADOS
        {
            "arquivo": "04-comandos-avancados.md",
            "conteudo": r"""# 🚀 Comandos Avançados no Vim

> **Objetivo:** Explorar técnicas avançadas que elevam sua proficiência para o próximo nível.

## Exercício 1: Text Objects
```javascript
const usuario = {
    nome: "Carlos Silva",
    email: "carlos@exemplo.com",
    idade: 34,
    perfil: {
        nivel: "admin",
        ativo: true
    }
};
```

Experimente estes comandos posicionando o cursor dentro das aspas ou parênteses:
- \`ci"\` - Change Inside " (muda o texto dentro das aspas)
- \`da{\` - Delete Around { (deleta chaves e conteúdo)
- \`yi(\` - Yank Inside ( (copia o conteúdo dentro dos parênteses)
- \`va]\` - Visual Around ] (seleciona colchetes e conteúdo)

## Exercício 2: Macros
```
1. Posicione o cursor na primeira linha abaixo
2. Pressione 'qa' para iniciar gravação na macro 'a'
3. Execute: I- [ ] <Esc>j
4. Pressione 'q' para finalizar a gravação
5. Use '@a' para aplicar a macro e '5@a' para repetir 5 vezes

Item um
Item dois
Item três
Item quatro
Item cinco
```

## Exercício 3: Dobras (Folding)
```python
# Experimente comandos de dobra:
# zf3j - cria uma dobra das próximas 3 linhas
# zo - abre uma dobra
# zc - fecha uma dobra
# zR - abre todas as dobras
# zM - fecha todas as dobras

def funcao_principal():
    # Esta função contém várias partes
    # que podem ser dobradas para melhor visualização
    
    # Inicialização
    variaveis = preparar_ambiente()
    configurar_sistema()
    
    # Processamento principal
    for item in variaveis:
        processar(item)
        registrar_resultado(item)
    
    # Finalização
    limpar_recursos()
    return gerar_relatorio()
```

## Exercício 4: Janelas Múltiplas
```
Experimente estes comandos:
- :sp (divide horizontalmente)
- :vsp (divide verticalmente)
- Ctrl+w seguido de h,j,k,l (navega entre janelas)
- Ctrl+w seguido de + ou - (redimensiona altura)
- Ctrl+w seguido de < ou > (redimensiona largura)
- Ctrl+w seguido de = (equaliza tamanhos)
```

## 💡 Dicas de Edição Avançada
- `ci(` muda conteúdo dentro de parênteses (também funciona com `{`, `[`, `"`, `'`, etc.)
- `di(` deleta conteúdo dentro de parênteses
- `yi(` copia conteúdo dentro de parênteses
- `v` inicia seleção visual por caractere
- `V` inicia seleção visual por linha
- `Ctrl+v` inicia seleção visual por bloco
- `=` reindenta o código selecionado
- `>` aumenta a indentação
- `<` diminui a indentação
- `q{letra}` inicia gravação de macro no registro especificado
- `@{letra}` executa a macro do registro especificado
- `:split` ou `:sp` divide a janela horizontalmente
- `:vsplit` ou `:vsp` divide a janela verticalmente
- `Ctrl+w` seguido de `h`, `j`, `k`, `l` navega entre janelas


> **Dica:** Estes comandos avançados têm uma curva de aprendizado mais íngreme, mas o investimento de tempo vale a pena pela enorme produtividade que proporcionam!
""",
        },
        # MODOS VISUAL E COMANDO
        {
            "arquivo": "05-modos-visual-comando.md",
            "conteudo": """# 👁️ Modos Visual e de Comando no Vim

## 🎯 Objetivos de Aprendizado
- Utilizar seleção visual para edições complexas
- Trabalhar com indentação e formatação de código
- Uso funcional de macros no neovim

## Exercício 1: Seleção Visual Básica
```
const produtos = [
  { id: 1, nome: "Smartphone", preco: 1299.99, estoque: 50 },
  { id: 2, nome: "Notebook", preco: 4500.00, estoque: 20 },
  { id: 3, nome: "Monitor", preco: 800.00, estoque: 30 },
  { id: 4, nome: "Teclado", preco: 100.00, estoque: 100 },
  { id: 5, nome: "Mouse", preco: 50.00, estoque: 150 }
];

// Implementar função para calcular valor total em estoque
```

### Tarefas:
1. [ ] Use o modo visual com `v` para selecionar "Smartphone" e substitua por "Celular"
2. [ ] Use o modo visual de linha `V` para selecionar a primeira linha de produtos e copie com `y`
3. [ ] Cole após o último produto e edite para um novo produto
4. [ ] Use o modo visual de bloco `Ctrl+v` para selecionar os preços, movendo para baixo com `j`
5. [ ] Adicione a moeda R$ antes de cada preço usando `I` no modo visual de bloco
6. [ ] Abaixo do comentário, adicione a implementação da função usando `o`

## Exercício 2: Seleção Visual em Bloco
```
nome1    email1@exemplo.com    ativo
nome2    email2@exemplo.com    inativo
nome3    email3@exemplo.com    ativo
nome4    email4@exemplo.com    inativo
nome5    email5@exemplo.com    ativo
```

1. Posicione o cursor no 'e' de "email1"
2. Pressione Ctrl+v para entrar no modo visual de bloco
3. Pressione 2j para selecionar também as duas linhas abaixo
4. Pressione I para inserir no início da seleção
5. Digite "EMAIL: " e pressione Esc

## 📝 Exercício 3: Indentação e Formatação

```html
<div class="container">
<h1>Título da Página</h1>
<p>Este é um parágrafo com <strong>texto em negrito</strong> e <em>texto em itálico</em>.</p>
<ul>
<li>Item 1</li>
<li>Item 2</li>
<li>Item 3</li>
</ul>
<div class="footer">
<p>Rodapé da página</p>
</div>
</div>
```

### Tarefas:
1. [ ] Selecione todo o conteúdo com `gg` para ir ao topo e depois `VG` para selecionar até o final
2. [ ] Reindente todo o HTML usando `=` no modo visual
3. [ ] Use `>` para aumentar a indentação da lista `<ul>` inteira (selecione com `V`)
4. [ ] Use `<` para diminuir a indentação do rodapé inteiro

## 📝 Exercício 4: Macros

```python
# Lista de produtos para formatar
produto_1 = "Caneta"
preco_1 = 2.50
estoque_1 = 100

produto_2 = "Caderno"
preco_2 = 15.00
estoque_2 = 50

produto_3 = "Borracha"
preco_3 = 1.00
estoque_3 = 200

# Vamos transformar em dicionários
produtos = []
# Adicione os produtos aqui
```

### Tarefas:
1. [ ] Posicione o cursor na linha de `produto_1`
2. [ ] Inicie a gravação de uma macro no registro `q` usando `qq`
3. [ ] Crie um comando para transformar as 3 linhas em um dicionário no formato:
   ```python
   produtos.append({
       "nome": "Caneta",
       "preco": 2.50,
       "estoque": 100
   })
   ```
4. [ ] Termine a gravação com `q`
5. [ ] Execute a macro para os produtos 2 e 3 usando `@q`

## 📝 Exercício 5: Múltiplos Arquivos

### Arquivo 1: `config.py`
```python
# Configurações do sistema
DEBUG = True
HOST = "localhost"
PORT = 8000
DATABASE = "sqlite:///app.db"
```

### Arquivo 2: `app.py`
```python
# Importe as configurações
# TODO: Adicionar imports

def iniciar_aplicacao():
    # Use as configurações aqui
    print(f"Server running on {HOST}:{PORT}")
    print(f"Debug mode: {DEBUG}")
    
if __name__ == "__main__":
    iniciar_aplicacao()
```

### Tarefas:
1. [ ] Abra ambos os arquivos com `vim -o config.py app.py`
2. [ ] Alterne entre os arquivos usando `Ctrl+w` seguido de `h` ou `l`
3. [ ] Em `app.py`, adicione `from config import DEBUG, HOST, PORT, DATABASE` após o comentário de imports
4. [ ] Use `:w` para salvar as alterações sem sair
5. [ ] Use `:qa` para sair de todos os arquivos


## Exercício 6: Comandos Ex
```
Experimente estes comandos no modo de comando (após :)

:set number - Mostra números de linha
:set nonumber - Oculta números de linha
:syntax on - Ativa syntax highlighting
:set hlsearch - Destaca resultados de busca
:nohl - Remove destaques de busca
:w - Salva o arquivo
:e arquivo.txt - Edita outro arquivo
:help comando - Abre ajuda sobre algum comando
```

## Exercício 7: Faixas de Linha
```html
<!-- Experimente selecionar faixas de linha com comandos: -->
<!-- :3,6d - Deleta as linhas 3 a 6 -->
<!-- :10,15y - Copia as linhas 10 a 15 -->
<!-- :20,25s/antigo/novo/g - Substitui nas linhas 20-25 -->

<header>
  <nav>
    <ul>
      <li>Item 1</li>
      <li>Item 2</li>
      <li>Item 3</li>
    </ul>
  </nav>
</header>
<main>
  <section>
    <h1>Título Principal</h1>
    <p>Parágrafo 1</p>
    <p>Parágrafo 2</p>
  </section>
</main>
```

## 🚀 Desafio Bônus
Crie uma macro para formatar um conjunto de dados CSV em uma tabela HTML com tags `<table>`, `<tr>`, e `<td>`.

> **Dica:** O modo visual torna a edição de faixas de texto muito mais intuitiva, enquanto o modo de comando oferece operações poderosas e precisas sobre faixas de linhas!""",
        },
        # OPERADORES E REPETIÇÃO
        {
            "arquivo": "06-operadores-repeticao.md",
            "conteudo": """# 🔄 Operadores e Repetição no Vim

> **Objetivo:** Aprender a usar operadores em combinação com movimentos e dominar técnicas de repetição para edições eficientes.

## Exercício 1: Operadores Básicos
```
Operador + Movimento = Ação

Experimente estas combinações (posicione o cursor no início das palavras):
- dw - Delete Word (deleta uma palavra)
- d$ - Delete até o fim da linha
- ce - Change até o fim da palavra
- ct, - Change até a próxima vírgula
- yt) - Yank (copia) até o próximo parêntese
- df: - Delete até e incluindo o próximo dois-pontos
```

## Exercício 2: Repetição com Ponto
```python
# O comando '.' repete a última alteração. Experimente:
variavel_1 = "valor"  # Mude para variavel_um usando cw
variavel_2 = "valor"  # Posicione o cursor aqui e use apenas '.'
variavel_3 = "valor"  # Use '.' novamente
variavel_4 = "valor"  # E mais uma vez...
```

## Exercício 3: Contadores
```html
<!-- Use contadores para repetir comandos -->
<div>Primeiro item</div>  <!-- Posicione aqui e use dd para deletar -->
<div>Segundo item</div>   <!-- Use 3dd para deletar 3 linhas de uma vez -->
<div>Terceiro item</div>
<div>Quarto item</div>
<div>Quinto item</div>    <!-- Use 2dj para deletar esta e a próxima -->
<div>Sexto item</div>
```

## Exercício 4: Operadores Compostos
```javascript
// Experimente estas operações compostas:
const configuracao = {
    tema: "escuro",    // Use ciw para Change Inner Word
    fonte: "Arial",    // Use yi" para Yank Inside quotes
    tamanho: 14,       // Use 2dw para Delete 2 Words
    opções: {          // Use da{ para Delete Around braces
        negrito: true,
        itálico: false,
        sublinhado: true
    }
};
```

> **Dica:** A verdadeira potência do Vim vem da combinação inteligente de operadores e movimentos. Quando você domina estas combinações e aprende a repetir ações, sua velocidade de edição aumenta dramaticamente!
""",
        },
        # CONFIGURAÇÃO E PERSONALIZAÇÃO
        {
            "arquivo": "07-configuracao-personalizacao.md",
            "conteudo": """# ⚙️ Configuração e Personalização do Vim

> **Objetivo:** Aprender a personalizar o Vim para seu fluxo de trabalho e descobrir ajustes que aumentam sua produtividade.

## Exercício 1: Ajustes Básicos do .vimrc
```vim
" Edite seu ~/.vimrc para incluir estas configurações básicas:
set number          " Mostra números de linha
set relativenumber  " Números relativos à linha atual
set hlsearch        " Destaca resultados de busca
set incsearch       " Busca incremental ao digitar
set ignorecase      " Ignora maiúsculas/minúsculas na busca
set smartcase       " Sensível a maiúsculas se incluídas no termo

" Adicione este mapeamento e teste-o no editor:
" (pressione a tecla de espaço seguida de 'w' para salvar)
nnoremap <space>w :w<CR>
```

## Exercício 2: Cores e Tema
```vim
" Experimente diferentes esquemas de cores:
:colorscheme desert
:colorscheme slate
:colorscheme morning
:colorscheme evening

" Adicione ao seu .vimrc para tornar permanente:
set background=dark  " ou light
colorscheme slate    " ou seu preferido
syntax enable        " Habilita syntax highlighting
```

## Exercício 3: Mapeamentos Úteis
```vim
" Experimente criar mapeamentos para operações frequentes:

" Pressione F5 para executar o arquivo Python atual
nnoremap <F5> :!python %<CR>

" Use Ctrl+j e Ctrl+k para mover linhas para baixo e para cima
nnoremap <C-j> :m +1<CR>
nnoremap <C-k> :m -2<CR>

" Leader+s para substituir a palavra sob o cursor em todo o arquivo
nnoremap <leader>s :%s/\\<<C-r><C-w>\\>//g<left><left>
```

## Exercício 4: Plugins Essenciais
```vim
" Se você usa vim-plug, adicione estes plugins ao seu .vimrc:

call plug#begin('~/.vim/plugged')

" NERDTree - explorador de arquivos
Plug 'preservim/nerdtree'
" Mapeamento: Ctrl+n para abrir/fechar
nnoremap <C-n> :NERDTreeToggle<CR>

" vim-surround - manipular delimitadores
Plug 'tpope/vim-surround'
" Use cs"' para mudar aspas duplas para simples

" fzf - busca fuzzy
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
" Mapeamento: Ctrl+p para buscar arquivos
nnoremap <C-p> :Files<CR>

call plug#end()
```

> **Dica:** A personalização é uma parte fundamental do Vim! Seu .vimrc deve evoluir com o tempo, à medida que você descobre seu fluxo de trabalho ideal. Adicione mudanças graduais e documente-as com comentários para lembrar o que cada configuração faz.
""",
        },
        # INTEGRAÇÃO COM TERMINAL E GIT
        {
            "arquivo": "08-terminal-git.md",
            "conteudo": """# 🖥️ Vim com Terminal e Git

> **Objetivo:** Aprender a integrar o Vim com o terminal e ferramentas de controle de versão para um fluxo de trabalho completo.

## Exercício 1: Terminal Integrado
```
Experimente estes comandos para interagir com o terminal:

:! ls -la                  # Executa comando ls e mostra a saída
:term                      # Abre terminal integrado (Vim 8+/Neovim)
Ctrl+w N                   # Entra no modo normal dentro do terminal

No Neovim, experimente:
:split | terminal          # Terminal em split horizontal
:vsplit | terminal         # Terminal em split vertical
```

## Exercício 2: Git Básico
```bash
# Experimente estes comandos Git dentro do Vim:
:!git status               # Verifica o status do repositório
:!git add %                # Adiciona o arquivo atual
:!git commit -m "Mensagem" # Faz um commit
:!git diff %               # Mostra diferenças no arquivo atual
:!git log -p %             # Histórico do arquivo atual
```

## Exercício 3: Plugin vim-fugitive
```vim
" Se você tem vim-fugitive instalado, tente:
:G                     " Equivalente a :!git status
:Gdiff                 " Diff vertical do arquivo atual
:Gblame                " Mostra quem modificou cada linha
:Gcommit               " Inicia commit
:Gpush                 " Push para remote
:Gpull                 " Pull do remote

" Em um arquivo com conflitos de merge:
:Gdiff                 " Para resolver visualmente
```

## Exercício 4: Sessões e Projetos
```vim
" Experimente gerenciar sessões:

" Salvar sessão atual (janelas, buffers, etc):
:mksession ~/projeto-sessao.vim

" Restaurar sessão:
:source ~/projeto-sessao.vim
" Ou ao abrir o Vim:
" vim -S ~/projeto-sessao.vim

" Com plugin vim-obsession:
:Obsession ~/projeto-sessao.vim  " Salva e atualiza automaticamente
```

> **Dica:** A integração com terminal e Git torna o Vim um ambiente de desenvolvimento completo. Invista tempo aprendendo plugins como vim-fugitive e vim-gitgutter para melhorar ainda mais sua experiência com controle de versão!
""",
        },
        # REFATORAÇÃO E CÓDIGO INTELIGENTE
        {
            "arquivo": "09-refatoracao-codigo.md",
            "conteudo": """# 🧠 Refatoração e Código Inteligente

> **Objetivo:** Dominar técnicas avançadas para manipulação e refatoração de código de forma eficiente.

## Exercício 1: Indentação Inteligente
```python
# Experimente os comandos de indentação:
# Posicione o cursor em def e pressione '>}' para indentar o bloco

def funcao_mal_indentada():
code = "isto deveria estar indentado"
for i in range(10):
print(i)  # deveria estar indentado duas vezes
if i > 5:
break  # deveria estar indentado três vezes

# Agora faça o mesmo com '=}' para formatação automática
# A diferença é que '=' tenta seguir as regras de indentação da linguagem
```

## Exercício 2: Refatoração de Variáveis
```javascript
// Pratique renomear variáveis em múltiplos locais:
function calcularTotal(items) {
    let soma = 0;
    for (let i = 0; i < items.length; i++) {
        soma += items[i].preco;
    }
    return "Valor total: " + soma;
}

// Use * para buscar 'soma' e depois:
// cgn para substituir a primeira ocorrência
// Use . (ponto) para repetir nas próximas ocorrências
// Altere 'soma' para 'valorTotal' em todas as ocorrências
```

## Exercício 3: Extração de Método
```python
def processar_pedido(pedido):
    # Este bloco deve ser extraído para uma nova função 'calcular_imposto'
    base_imposto = pedido.valor * 0.9
    if pedido.estado == "SP":
        imposto = base_imposto * 0.12
    elif pedido.estado == "RJ":
        imposto = base_imposto * 0.15
    else:
        imposto = base_imposto * 0.10
        
    # Continue com o processamento...
    pedido.total = pedido.valor + imposto
    pedido.prazo = calcular_prazo_entrega(pedido)
    return pedido
```

## Exercício 4: Macros para Padrões Repetitivos
```html
<!-- Use macros para transformar este HTML: -->
<div>Item 1</div>
<div>Item 2</div>
<div>Item 3</div>

<!-- Em uma lista: -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
  <li>Item 3</li>
</ul>

<!-- Dica: Comece gravando com qa, depois: -->
<!-- I<li><ESC>f<i</li><ESC>j -->
<!-- Execute a macro com @a nas linhas restantes -->
```

> **Dica:** A combinação de macros, marcadores e operações de texto torna o Vim extremamente poderoso para refatorações. Com prática, você pode realizar em segundos alterações que levariam minutos em outros editores!
""",
        },
        # EXERCÍCIOS DE FLUXO COMPLETO
        {
            "arquivo": "10-fluxo-completo.md",
            "conteudo": """# 🔄 Fluxo de Trabalho Completo

## 🎯 Objetivos de Aprendizado
- Dominar fluxos de trabalho eficientes combinando comandos
- Aprender a personalizar o Vim para suas necessidades
- Resolver problemas comuns de desenvolvimento com o Vim
> Integrar diversos comandos em fluxos de trabalho realistas que simulam tarefas cotidianas de desenvolvimento.

## 📝 Exercício 1: Refatoração de API
```javascript
// Este é um arquivo de API que precisa ser refatorado
// Siga os passos abaixo usando comandos Vim eficientes

// 1. Renomeie a função getUser para getUserById (use :%s/getUser/getUserById/g)
function getUser(id) {
  return database.users.findById(id);
}

// 2. Adicione validação de parâmetros (use o para criar linha abaixo e entrar no modo insert)
function createUser(userData) {
  // Adicione aqui: if (!userData.name || !userData.email) throw new Error("Dados inválidos");
  return database.users.create(userData);
}

// 3. Extraia uma função de validação reutilizável (selecione com V e use y para copiar)
function updateUser(id, userData) {
  if (!id) throw new Error("ID é obrigatório");
  return database.users.update(id, userData);
}

// 4. Use ctags ou navegação com gd/gf para encontrar definições (isto é apenas demonstrativo)
function deleteUser(id) {
  return database.users.delete(id);
}

// 5. Adicione documentação JSDoc acima de cada função (use O para criar linha acima)
```

## 📝 Exercício 1.1: Refatoração de Código

```python
# Este código precisa ser refatorado
def calcular_total(lista_de_precos):
    total = 0
    for preco in lista_de_precos:
        total = total + preco
    return total

def calcular_media(lista_de_precos):
    total = 0
    for preco in lista_de_precos:
        total = total + preco
    return total / len(lista_de_precos)

def calcular_maximo(lista_de_precos):
    maximo = lista_de_precos[0]
    for preco in lista_de_precos:
        if preco > maximo:
            maximo = preco
    return maximo

def calcular_minimo(lista_de_precos):
    minimo = lista_de_precos[0]
    for preco in lista_de_precos:
        if preco < minimo:
            minimo = preco
    return minimo
```

### Tarefas:
1. [ ] Extraia a lógica repetida em uma função auxiliar chamada `_calcular_soma`
2. [ ] Use `y%` para copiar um bloco inteiro de função (do início ao fim)
3. [ ] Use `:s` para mudar os nomes e implementar a função auxiliar
4. [ ] Refatore as outras funções para usar a nova função auxiliar
5. [ ] Use `gqq` para formatar linhas muito longas

## Exercício 2: Debug com Logs
```python
def processar_transacao(transacao):
    # 1. Adicione logs estratégicos (use o para adicionar linhas)
    # 2. Use marcadores para navegar entre pontos importantes (ma, mb, 'a, 'b)
    
    # Valide a transação
    if not transacao.validar():
        # Adicione um log aqui com O: print(f"Transação inválida: {transacao.id}")
        return False
    
    # Processe o pagamento
    resultado = gateway_pagamento.processar(
        transacao.valor,
        transacao.cartao,
        transacao.parcelas
    )
    
    # Registre o resultado
    # Adicione um log aqui: print(f"Resultado: {resultado.status}")
    
    # Atualize o banco de dados
    if resultado.aprovado:
        atualizar_status(transacao.id, "APROVADO")
    else:
        # Definir marcador com ma aqui
        atualizar_status(transacao.id, "REJEITADO")
        # Use 'a para voltar aqui rapidamente
        enviar_notificacao(transacao.usuario, "Pagamento rejeitado")
    
    return resultado.aprovado
```

## Exercício 3: Navegação Multi-arquivo
```
Imagine que você está trabalhando em um projeto com múltiplos arquivos.
Use estas técnicas para navegar entre eles eficientemente:

### Projeto de API REST:

1. `models.py`:
```python
class Usuario:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email
```

2. `views.py`:
```python
# Importar modelos necessários

def listar_usuarios():
    # Todo: implementar listagem
    pass

def obter_usuario(id):
    # Todo: implementar busca por id
    pass

def criar_usuario(dados):
    # Todo: implementar criação
    pass
```

3. `urls.py`:
```python
# Importar controllers

def configurar_rotas(app):
    # Todo: configurar endpoints da API
    pass
```

### Tarefas:
1. [ ] Navegue entre os arquivos usando `:next` e `:prev`
2. [ ] Em `views.py`, adicione `from models import Usuario`
3. [ ] Implemente a função `listar_usuarios()` que retorne uma lista de usuários fictícios
4. [ ] Em `urls.py`, adicione `from controllers import listar_usuarios, obter_usuario, criar_usuario`
5. [ ] Implemente a função de configuração de rotas
6. [ ] Use marcas para pular facilmente entre pontos importantes com `m{letra}` e `'{letra}````

## Exercício 4: Refatoração HTML/CSS
```html
<!-- Refatore este HTML usando comandos Vim eficientes -->
<div class="container">
    <div class="header">
        <h1 class="title">Título do Site</h1>
        <div class="nav">
            <ul>
                <li class="nav-item">Home</li>
                <li class="nav-item">Produtos</li>
                <li class="nav-item">Contato</li>
            </ul>
        </div>
    </div>
    <div class="content">
        <p>Conteúdo do site</p>
    </div>
</div>

<!-- Tarefas: -->
<!-- 1. Converta todas as classes usando o BEM (:%s/nav-item/nav__item/g) -->
<!-- 2. Use Ctrl+v para seleção em bloco e adicione "active" à primeira li -->
<!-- 3. Use visual mode + > para indentar corretamente -->
<!-- 4. Use ci" para mudar o texto "Conteúdo do site" -->
```

## 📝 Exercício 3: Trabalho com Arquivos de Configuração

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "Uma aplicação de exemplo",
  "scripts": {
    "start": "node index.js",
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {
    "express": "^4.17.1",
    "mongoose": "^5.12.3",
    "dotenv": "^8.2.0"
  },
  "devDependencies": {
    "jest": "^26.6.3",
    "eslint": "^7.24.0"
  }
}
```

### Tarefas:
1. [ ] Atualize a versão para "1.1.0" usando `ci"`
2. [ ] Adicione um novo script "build" usando `ea` após a linha "lint"
3. [ ] Adicione uma nova dependência "axios" versão "^0.21.1"
4. [ ] Ordene as dependências alfabeticamente usando marcas e movimentação de linhas
5. [ ] Faça o arquivo ficar perfeitamente formatado com espaços e indentação corretos

## 📝 Exercício 4: Personalização do Vim

Crie um arquivo `.vimrc` a partir do zero:

```vim
" Arquivo .vimrc básico

" Configurações Básicas
set number          " Mostrar números de linha
set tabstop=4       " Tamanho do tab
set shiftwidth=4    " Tamanho da indentação
set expandtab       " Usa espaços em vez de tabs
set autoindent      " Indentação automática

" Mapeamentos Personalizados
" TODO: Adicionar mapeamentos úteis

" Plugins (comentado, requer gerenciador)
" TODO: Adicionar plugins recomendados
```

### Tarefas:
1. [ ] Adicione mais configurações básicas úteis como `syntax on` e `set relativenumber`
2. [ ] Adicione mapeamentos personalizados, como `map <leader>w :w<CR>` para salvar com `\\w`
3. [ ] Configure o destaque de busca com `set hlsearch` e `set incsearch`
4. [ ] Adicione um comentário para instalação de um gerenciador de plugins como vim-plug
5. [ ] Configure cores e tema com `colorscheme`

## 📝 Exercício 5: Resolução de Conflitos Git

```
<<<<<<< HEAD
function getUserData(userId) {
  return fetch(`/api/users/${userId}`)
    .then(response => response.json())
    .then(data => {
      console.log('User data retrieved');
      return data;
    });
}
=======
async function getUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    const userData = await response.json();
    console.log('User data retrieved successfully');
    return userData;
  } catch (error) {
    console.error('Failed to get user data', error);
    return null;
  }
}
>>>>>>> feature/async-refactor
```

> **Dica:** A verdadeira proficiência no Vim vem ao combinar comandos em fluxos de trabalho completos. A prática consistente destes cenários realistas transformará você em um usuário Vim muito mais eficiente!
""",
        },
    ]

    # Criar diretório se não existir
    os.makedirs("vim_practice", exist_ok=True)

    # Criar arquivos de exercícios
    for ex in exercicios:
        with open(f"vim_practice/{ex['arquivo']}", "w") as f:
            f.write(ex["conteudo"])
    print("\n✅ Exercícios gerados em /vim_practice!")
    print("💡 Dica: Execute 'vim -O vim_practice/*.md' para começar!")


def main():
    print("""
██╗   ██╗██╗███╗   ███╗    ██╗     ██╗██╗  ██╗███████╗     █████╗     ██████╗ ██████╗  ██████╗ 
██║   ██║██║████╗ ████║    ██║     ██║██║ ██╔╝██╔════╝    ██╔══██╗    ██╔══██╗██╔══██╗██╔═══██╗
██║   ██║██║██╔████╔██║    ██║     ██║█████╔╝ █████╗      ███████║    ██████╔╝██████╔╝██║   ██║
╚██╗ ██╔╝██║██║╚██╔╝██║    ██║     ██║██╔═██╗ ██╔══╝      ██╔══██║    ██╔═══╝ ██╔══██╗██║   ██║
 ╚████╔╝ ██║██║ ╚═╝ ██║    ███████╗██║██║  ██╗███████╗    ██║  ██║    ██║     ██║  ██║╚██████╔╝
  ╚═══╝  ╚═╝╚═╝     ╚═╝    ╚══════╝╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ 
    """)
    print("\n" + "=" * 50)
    print("         Treine seus comandos Vim aqui!       ")
    print("=" * 50 + "\n")
    print("1. 📝🧠 Iniciar Quiz Interativo")
    print("2. 🧪✅ Gerar Exercícios Práticos")
    print("3. ❌ Sair")

    opcao = input("\nEscolha uma opção: ").strip()

    if opcao == "1":
        quiz()
    elif opcao == "2":
        gerar_exercicio_pratico()
    else:
        print("\n👋 Até logo! Continue praticando!")


if __name__ == "__main__":
    main()
