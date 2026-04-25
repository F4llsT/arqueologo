import os
import sys
import json
from urllib.request import urlopen, Request

PROMPT_INTERNO = '''Você é um Arqueólogo de Código Especialista. Analise o código a seguir e gere uma documentação técnica impecável. Retorne EXCLUSIVAMENTE Markdown.

# 📄 Análise de Arquivo: [Nome do Arquivo]

## 🎯 Propósito Geral
[Explicação do que o código faz]

## ⚙️ Funções e Lógica Principal
* [nome_da_funcao](): [Explicação]

## 🚩 Problemas Identificados
[Liste code smells, variáveis mágicas, etc]

## 🛠️ Sugestão de Refatoração (Clean Code)
(Abaixo, escreva a versão refatorada e limpa do código)
'''

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        prompt = PROMPT_INTERNO.replace('[Nome do Arquivo]', os.path.basename(file_path)) + "\n\nCÓDIGO:\n" + code
        data = json.dumps({"model": "qwen2.5-coder:7b", "stream": False, "prompt": prompt}).encode('utf-8')
        req = Request("http://localhost:11434/api/generate", data=data, headers={'Content-Type': 'application/json'})
        
        print(f"[PROCESSANDO] {file_path}...")
        with urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            doc = result.get('response', '')

        os.makedirs("documentacao_gerada", exist_ok=True)
        out_path = os.path.join("documentacao_gerada", f"{os.path.basename(file_path)}_doc.md")
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"[SUCESSO] Salvo em: {out_path}")
    except Exception as e:
        print(f"[ERRO] Falha em {file_path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 arqueologo.py <diretorio>")
        sys.exit(1)
    
    target = sys.argv[1]
    if not os.path.isdir(target):
        print(f"[ERRO] Diretório '{target}' inválido.")
        sys.exit(1)

    print("[INICIO DO PROCESSO]")
    for root, _, files in os.walk(target):
        for file_name in files:
            if file_name.endswith('.py') and file_name != 'arqueologo.py':
                process_file(os.path.join(root, file_name))
    print("[CONCLUIU] Todas as operações foram concluídas.")

if __name__ == "__main__":
    main()
