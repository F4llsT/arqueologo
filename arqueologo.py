import os
import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError

# Configurações do Modelo e API Local
MODELO_IA = "qwen2.5-coder:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# O prompt usa crases triplas internas, por isso a formatação precisa ser cuidadosa
PROMPT_INTERNO = """Você é um Arqueólogo de Código Especialista em Engenharia Reversa e Clean Code. 
Analise o código a seguir e gere uma documentação técnica impecável. 
Retorne EXCLUSIVAMENTE o conteúdo em Markdown, sem conversas paralelas.

# 📄 Análise de Arquivo: [Nome do Arquivo]

## 🎯 Propósito Geral
[Explicação clara e concisa do que o código faz]

## ⚙️ Funções e Lógica Principal
* [nome_da_funcao](): [Explicação da responsabilidade]

## 🚩 Problemas Identificados
[Liste code smells, variáveis mágicas, falta de tipagem ou lógica confusa]

## 🛠️ Sugestão de Refatoração (Clean Code)
```python
# Versão refatorada e limpa do código aqui
```
"""

def process_file(file_path):
    """Lê o arquivo, processa na IA e salva o relatório."""
    try:
        if not file_path.endswith('.py'):
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        nome_arquivo = os.path.basename(file_path)
        prompt_final = PROMPT_INTERNO.replace('[Nome do Arquivo]', nome_arquivo) + "\n\nCÓDIGO FONTE:\n" + code

        payload = {
            "model": MODELO_IA,
            "stream": False,
            "prompt": prompt_final
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"🔍 Escavando: {nome_arquivo}...")
        
        with urlopen(req, timeout=None) as response:
            result = json.loads(response.read().decode('utf-8'))
            documentacao = result.get('response', '')

        # Garante a pasta de saída
        os.makedirs("documentacao_gerada", exist_ok=True)
        out_path = os.path.join("documentacao_gerada", f"{nome_arquivo}_doc.md")
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(documentacao)
        
        print(f"✨ Sucesso: {out_path}")

    except URLError:
        print(f"❌ Erro: Ollama offline em {OLLAMA_URL}")
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 arqueologo.py <caminho>")
        sys.exit(1)
    
    target = sys.argv[1]

    if not os.path.exists(target):
        print(f"❌ Erro: '{target}' não encontrado.")
        sys.exit(1)

    print("🚀 [ARQUEÓLOGO] Iniciando análise...")

    if os.path.isfile(target):
        process_file(target)
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file_name in files:
                if file_name.endswith('.py') and file_name != 'arqueologo.py':
                    process_file(os.path.join(root, file_name))

    print("🏁 [CONCLUÍDO]")

if __name__ == "__main__":
    main()