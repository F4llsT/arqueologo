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

# Dicionário de Inteligência: Mapeia a extensão do arquivo para a linguagem real
MAPA_LINGUAGENS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cs': 'C#',
    '.cpp': 'C++',
    '.c': 'C',
    '.go': 'Go',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.html': 'HTML',
    '.css': 'CSS'
}

# O Prompt agora possui a variável [Linguagem]
PROMPT_INTERNO = """Você é um Arqueólogo de Código Especialista Sênior em [Linguagem] e focado em Clean Code. 
Analise o código a seguir e gere uma documentação técnica impecável. 
Retorne EXCLUSIVAMENTE o conteúdo em Markdown, sem conversas paralelas.

# 📄 Análise de Arquivo: [Nome do Arquivo]

## 🎯 Propósito Geral
[Explicação clara e concisa do que o código faz]

## ⚙️ Funções e Lógica Principal
* [nome_da_funcao](): [Explicação da responsabilidade]

## 🚩 Problemas Identificados
[Liste code smells, variáveis mágicas, falta de tipagem ou lógica confusa específicos de [Linguagem]]

## 🛠️ Sugestão de Refatoração (Clean Code)
```[extensao_markdown]
# Versão refatorada e limpa do código aqui, seguindo as melhores práticas de [Linguagem]
```
"""

def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def carregar_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_cache(cache):
    os.makedirs("documentacao_gerada", exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)

def process_file(file_path):
    try:
        # 1. IDENTIFICAÇÃO DINÂMICA DE LINGUAGEM
        extensao = os.path.splitext(file_path)[1].lower()
        
        # Se for um arquivo que não conhecemos (ex: .txt, .md), ignoramos
        if extensao not in MAPA_LINGUAGENS:
            return

        linguagem_nome = MAPA_LINGUAGENS[extensao]
        ext_markdown = extensao.replace('.', '') # Ex: .py vira py para o bloco de código
        
        nome_arquivo = os.path.basename(file_path)
        out_path = os.path.join("documentacao_gerada", f"{nome_arquivo}_doc.md")

        # 2. SISTEMA DE CACHE
        current_hash = get_file_hash(file_path)
        cache = carregar_cache()

        if cache.get(file_path) == current_hash and os.path.exists(out_path):
            print(f"⚡ [CACHE HIT] '{nome_arquivo}' ({linguagem_nome}) carregado instantaneamente.")
            return

        # 3. LEITURA E INJEÇÃO DE CONTEXTO NA IA
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Substitui as variáveis no prompt para focar na linguagem exata
        prompt_final = PROMPT_INTERNO.replace('[Nome do Arquivo]', nome_arquivo)
        prompt_final = prompt_final.replace('[Linguagem]', linguagem_nome)
        prompt_final = prompt_final.replace('[extensao_markdown]', ext_markdown)
        prompt_final += "\n\nCÓDIGO FONTE:\n" + code

        payload = {
            "model": MODELO_IA,
            "stream": False,
            "prompt": prompt_final
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"🔍 Escavando: {nome_arquivo} (Especialidade: {linguagem_nome})...")
        
        with urlopen(req, timeout=None) as response:
            result = json.loads(response.read().decode('utf-8'))
            documentacao = result.get('response', '')

        os.makedirs("documentacao_gerada", exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(documentacao)
        
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

    print("🚀 [ARQUEÓLOGO MULTILINGUAGEM] Iniciando análise...")

    if os.path.isfile(target):
        process_file(target)
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file_name in files:
                # Agora analisamos qualquer arquivo que esteja no nosso dicionário!
                extensao = os.path.splitext(file_name)[1].lower()
                if extensao in MAPA_LINGUAGENS and file_name != 'arqueologo.py':
                    process_file(os.path.join(root, file_name))

    print("🏁 [CONCLUÍDO]")

if __name__ == "__main__":
    main()