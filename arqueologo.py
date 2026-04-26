import os
import sys
import json
import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError

# Configurações do Modelo e API Local
MODELO_IA = "qwen2.5-coder:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"
CACHE_FILE = os.path.join("documentacao_gerada", "arqueologo_cache.json")

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

def get_file_hash(file_path):
    """Gera um hash MD5 baseado no conteúdo exato do arquivo."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def carregar_cache():
    """Lê o arquivo de cache JSON."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_cache(cache):
    """Salva o dicionário de cache no arquivo JSON."""
    os.makedirs("documentacao_gerada", exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)

def process_file(file_path):
    """Lê o arquivo, verifica o cache, processa na IA e salva o relatório."""
    try:
        if not file_path.endswith('.py'):
            return

        nome_arquivo = os.path.basename(file_path)
        out_path = os.path.join("documentacao_gerada", f"{nome_arquivo}_doc.md")

        # 1. LÓGICA DE CACHE (Alta Performance)
        current_hash = get_file_hash(file_path)
        cache = carregar_cache()

        # Verifica se o arquivo não mudou e se o relatório já existe
        if cache.get(file_path) == current_hash and os.path.exists(out_path):
            print(f"⚡ [CACHE HIT] O arquivo '{nome_arquivo}' não foi modificado. Carregando instantaneamente...")
            return  # Retorna imediatamente sem chamar a IA!

        # 2. SE NÃO TEM CACHE, LÊ O ARQUIVO E CHAMA A IA
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        prompt_final = PROMPT_INTERNO.replace('[Nome do Arquivo]', nome_arquivo) + "\n\nCÓDIGO FONTE:\n" + code

        payload = {
            "model": MODELO_IA,
            "stream": False,
            "prompt": prompt_final
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"🔍 Escavando: {nome_arquivo}...")
        
        # Mantendo timeout=None para a IA ter o tempo que precisar
        with urlopen(req, timeout=None) as response:
            result = json.loads(response.read().decode('utf-8'))
            documentacao = result.get('response', '')

        # Garante a pasta de saída e salva o documento
        os.makedirs("documentacao_gerada", exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(documentacao)
        
        # 3. ATUALIZA O CACHE PARA AS PRÓXIMAS EXECUÇÕES
        cache[file_path] = current_hash
        salvar_cache(cache)
        
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