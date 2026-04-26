import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

export function activate(context: vscode.ExtensionContext) {
    
    // =========================================================================
    // COMANDO 1: ARQUEÓLOGO CLÁSSICO (Arquivos e Pastas) - Documentação Permanente
    // =========================================================================
    let disposableArquivo = vscode.commands.registerCommand('arqueologo.analisarCodigo', async (uri: vscode.Uri) => {
        const targetPath = uri ? uri.fsPath : '';
        if (!targetPath) {
            vscode.window.showErrorMessage('❌ Selecione um arquivo ou pasta.');
            return;
        }

        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('❌ Abra uma pasta no VS Code primeiro.');
            return;
        }
        
        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const scriptPath = path.join(context.extensionPath, 'arqueologo.py');

        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage('⚠️ Motor arqueologo.py não encontrado.');
            return;
        }

        const targetName = path.basename(targetPath);
        const reportName = `${targetName}_doc.md`;
        
        // Caminho esperado: A pasta 'documentacao_gerada' na raiz do seu projeto
        const expectedDocPath = path.join(workspaceRoot, 'documentacao_gerada', reportName);

        // O CWD (Current Working Directory) é a raiz do projeto
        executarPython(scriptPath, targetPath, workspaceRoot, targetName, expectedDocPath, false);
    });

    // =========================================================================
    // COMANDO 2: ARQUEÓLOGO CIRÚRGICO (Texto Selecionado) - Volátil e Rápido
    // =========================================================================
    let disposableSelecao = vscode.commands.registerCommand('arqueologo.analisarSelecao', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('❌ Nenhum editor de texto ativo.');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        if (!text.trim()) {
            vscode.window.showWarningMessage('⚠️ Selecione um trecho de código primeiro.');
            return;
        }

        const scriptPath = path.join(context.extensionPath, 'arqueologo.py');
        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage('⚠️ Motor arqueologo.py não encontrado.');
            return;
        }

        // Obtém a extensão do arquivo atual para o Python identificar a linguagem
        const currentFilePath = editor.document.uri.fsPath;
        const extensao = path.extname(currentFilePath) || '.txt';

        // 🚀 A MÁGICA: Cria uma pasta temporária global do SISTEMA OPERACIONAL
        const tempWorkspace = path.join(os.tmpdir(), 'arqueologo_temp_workspace');
        if (!fs.existsSync(tempWorkspace)) {
            fs.mkdirSync(tempWorkspace, { recursive: true });
        }

        // Salva o texto selecionado num ficheiro temporário lá no sistema
        const tempFileName = `selecao_temporaria${extensao}`;
        const tempFilePath = path.join(tempWorkspace, tempFileName);
        fs.writeFileSync(tempFilePath, text, 'utf8');

        // Caminho esperado: O Python vai criar 'documentacao_gerada' DENTRO da pasta temporária
        const reportName = `${tempFileName}_doc.md`;
        const expectedDocPath = path.join(tempWorkspace, 'documentacao_gerada', reportName);

        // O CWD agora é a pasta temporária do sistema
        executarPython(scriptPath, tempFilePath, tempWorkspace, tempFileName, expectedDocPath, true);
    });

    context.subscriptions.push(disposableArquivo, disposableSelecao);
}

// =========================================================================
// FUNÇÃO AUXILIAR: Executa o Python e abre o relatório dinamicamente
// =========================================================================
function executarPython(scriptPath: string, targetPath: string, cwdPath: string, targetName: string, expectedDocPath: string, isTemp: boolean) {
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `🏺 Arqueólogo: Analisando ${isTemp ? 'trecho selecionado' : targetName}...`,
        cancellable: false
    }, (progress) => {
        return new Promise<void>((resolve) => {
            const pythonCmd = os.platform() === 'win32' ? 'python' : 'python3';
            const command = `${pythonCmd} "${scriptPath}" "${targetPath}"`;
            
            // O parâmetro `cwd` dita onde o Python vai criar a pasta "documentacao_gerada"
            exec(command, { cwd: cwdPath }, (error: Error | null, stdout: string, stderr: string) => {
                if (error) {
                    vscode.window.showErrorMessage(`❌ Erro de Execução: ${stderr || error.message}`);
                    resolve(); 
                    return;
                }

                if (fs.existsSync(expectedDocPath)) {
                    const openPath = vscode.Uri.file(expectedDocPath);
                    vscode.workspace.openTextDocument(openPath).then(doc => {
                        vscode.window.showTextDocument(doc, {
                            viewColumn: vscode.ViewColumn.Beside,
                            preserveFocus: false
                        });
                    });
                    
                    // Feedback visual verde apenas para a documentação permanente
                    if (!isTemp) {
                        vscode.window.showInformationMessage(`✅ Relatório de "${targetName}" pronto!`);
                    }
                } else {
                    vscode.window.showWarningMessage(`O relatório não foi gerado. Resposta do motor: ${stdout || "Sem resposta (O Python parou silenciosamente)"}`);
                }
                resolve();
            });
        });
    });
}

export function deactivate() {}