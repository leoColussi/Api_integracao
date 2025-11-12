import re
from collections import Counter

# Palavras reservadas
palavras_reservadas = {"if", "else", "while", "for", "return", "def", "class", "print"}

# Padrões de tokens
tokens = {
    "NUMERO": r"\d+(\.\d+)?",
    "IDENTIFICADOR": r"[a-zA-Z_]\w*",
    "OPERADOR": r"[+\-*/=<>!]+",
    "PARENTESE_ABRE": r"\(",
    "PARENTESE_FECHA": r"\)",
    "CHAVE_ABRE": r"\{",
    "CHAVE_FECHA": r"\}",
    "PONTO_VIRGULA": r";",
    "VIRGULA": r",",
    "DOIS_PONTOS": r":",
    "ESPACO": r"\s+",
}

# Cria uma regex combinada com grupos nomeados
padrao = "|".join(f"(?P<{nome}>{regex})" for nome, regex in tokens.items())

def tokenizar(codigo):
    """Função que percorre o código e gera tokens."""
    for match in re.finditer(padrao, codigo):
        tipo = match.lastgroup
        valor = match.group()
        if tipo == "ESPACO":
            continue
        if tipo == "IDENTIFICADOR" and valor in palavras_reservadas:
            tipo = "PALAVRA_RESERVADA"
        yield tipo, valor

# ==========================
# 🚀 Parte interativa
# ==========================

print("=== Analisador Léxico Simples ===")
print("Digite seu código (linha vazia para encerrar):")

# Coleta o código do usuário
linhas = []
while True:
    linha = input(">>> ")
    if not linha.strip():
        break
    linhas.append(linha)
codigo = "\n".join(linhas)

# Tokeniza o código
lista_tokens = list(tokenizar(codigo))
contagem = Counter(tipo for tipo, _ in lista_tokens)

# Exibe os tokens encontrados
print("\n--- Tokens encontrados ---")
for tipo, valor in lista_tokens:
    print(f"{tipo:<20} -> {valor}")

# Exibe resumo
print("\n--- Resumo dos tokens ---")
for tipo, qtd in contagem.items():
    print(f"{tipo:<20}: {qtd}")

print("\nAnálise concluída ✅")
