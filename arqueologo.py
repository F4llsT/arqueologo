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

# Dicionário de Inteligência
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

# PROMPT TURBINADO (Montado linha a linha para evitar erros de renderização)
P = []
P.append("Você é um Arqueólogo de Código e Especialista Sênior em Segurança Ofensiva (AppSec) em [Linguagem].")
P.append("Sua missão é realizar uma engenharia reversa profunda e uma auditoria de segurança no código fornecido.")
P.append("\nRetorne EXCLUSIVAMENTE o conteúdo em Markdown seguindo esta estrutura:\n")
P.append("# 📄 Análise de Arquivo: [Nome do Arquivo]")
P.append("\n## 🎯 Propósito Geral\n[Explicação clara e concisa do que o código faz]")
P.append("\n## 🚩 Problemas de Clean Code e Lógica\n* [item]: [explicação do code smell]")
P.append("\n## 🛡️ Auditoria de Segurança (Vulnerabilidades)")
P.append("> **Atenção:** Avaliação baseada nos padrões OWASP. Procure por Hardcoded Secrets, Injeções e falhas de lógica.")
P.append("\n* **[Nível de Risco]**: [Descrição técnica da falha]")
P.append("* **Impacto**: [O que um atacante poderia fazer]")
P.append("\n## 🛠️ Sugestão de Refatoração Segura")
P.append("```[extensao_markdown]\n# Versão refatorada aqui\n```")

PROMPT_INTERNO = "\n".join(P)

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except:
        return ""

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
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=4)
    except:
        pass

def process_file(file_path):
    try:
        extensao = os.path.splitext(file_path)[1].lower()
        if extensao not in MAPA_LINGUAGENS:
            return

        linguagem_nome = MAPA_LINGUAGENS[extensao]
        ext_markdown = extensao.replace('.', '')
        nome_arquivo = os.path.basename(file_path)
        out_path = os.path.join("documentacao_gerada", f"{nome_arquivo}_doc.md")

        current_hash = get_file_hash(file_path)
        cache = carregar_cache()

        if cache.get(file_path) == current_hash and os.path.exists(out_path):
            print(f"⚡ [CACHE] '{nome_arquivo}' carregado.")
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        p_final = PROMPT_INTERNO.replace('[Nome do Arquivo]', nome_arquivo)
        p_final = p_final.replace('[Linguagem]', linguagem_nome)
        p_final = p_final.replace('[extensao_markdown]', ext_markdown)
        p_final += "\n\nCÓDIGO FONTE:\n" + code

        payload = {"model": MODELO_IA, "stream": False, "prompt": p_final}
        data = json.dumps(payload).encode('utf-8')
        req = Request(OLLAMA_URL, data=data, headers={'Content-Type': 'application/json'})
        
        print(f"🔍 Auditando: {nome_arquivo}...")
        with urlopen(req, timeout=None) as response:
            result = json.loads(response.read().decode('utf-8'))
            documentacao = result.get('response', '')

        os.makedirs("documentacao_gerada", exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(documentacao)
        
        cache[file_path] = current_hash
        salvar_cache(cache)
        print(f"✨ Sucesso: {out_path}")

    except Exception as e:
        print(f"❌ Erro em {file_path}: {str(e)}")

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    target = sys.argv[1]
    if not os.path.exists(target):
        sys.exit(1)

    if os.path.isfile(target):
        process_file(target)
    elif os.path.isdir(target):
        for root, _, files in os.walk(target):
            for file_name in files:
                ext = os.path.splitext(file_name)[1].lower()
                if ext in MAPA_LINGUAGENS and file_name != 'arqueologo.py':
                    process_file(os.path.join(root, file_name))

if __name__ == "__main__":
    main()