import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

export function activate(context: vscode.ExtensionContext) {
    
    // =========================================================================
    // COMANDO 1: ARQUEÓLOGO CLÁSSICO (Arquivos e Pastas)
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

        executarPython(scriptPath, targetPath, workspaceRoot, path.basename(targetPath));
    });

    // =========================================================================
    // COMANDO 2: ARQUEÓLOGO CIRÚRGICO (Texto Selecionado)
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

        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('❌ Abra uma pasta no VS Code primeiro.');
            return;
        }

        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const scriptPath = path.join(context.extensionPath, 'arqueologo.py');

        // Pega a extensão do arquivo atual para o Python saber qual é a linguagem!
        const currentFilePath = editor.document.uri.fsPath;
        const extensao = path.extname(currentFilePath) || '.txt';

        // Cria uma pasta temporária invisível
        const tempDir = path.join(workspaceRoot, 'documentacao_gerada', '.temp');
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }

        // Salva o texto selecionado num arquivo "fantasma"
        const tempFileName = `selecao_temporaria${extensao}`;
        const tempFilePath = path.join(tempDir, tempFileName);
        fs.writeFileSync(tempFilePath, text, 'utf8');

        executarPython(scriptPath, tempFilePath, workspaceRoot, tempFileName);
    });

    context.subscriptions.push(disposableArquivo, disposableSelecao);
}

// =========================================================================
// FUNÇÃO AUXILIAR: Executa o Python e abre o relatório (Evita código duplicado)
// =========================================================================
function executarPython(scriptPath: string, targetPath: string, workspaceRoot: string, targetName: string) {
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `🏺 Arqueólogo: Analisando ${targetName}...`,
        cancellable: false
    }, (progress) => {
        return new Promise<void>((resolve) => {
            const pythonCmd = os.platform() === 'win32' ? 'python' : 'python3';
            const command = `${pythonCmd} "${scriptPath}" "${targetPath}"`;
            
            exec(command, { cwd: workspaceRoot }, (error: Error | null, stdout: string, stderr: string) => {
                if (error) {
                    vscode.window.showErrorMessage(`❌ Erro: ${stderr || error.message}`);
                    resolve(); 
                    return;
                }

                const reportName = `${targetName}_doc.md`;
                // Se for a seleção, ela salva dentro da pasta .temp. Senão, na raiz da documentacao_gerada.
                const isTemp = targetName.includes('selecao_temporaria');
                const docPath = isTemp 
                    ? path.join(workspaceRoot, 'documentacao_gerada', '.temp', reportName)
                    : path.join(workspaceRoot, 'documentacao_gerada', reportName);

                if (fs.existsSync(docPath)) {
                    const openPath = vscode.Uri.file(docPath);
                    vscode.workspace.openTextDocument(openPath).then(doc => {
                        vscode.window.showTextDocument(doc, {
                            viewColumn: vscode.ViewColumn.Beside,
                            preserveFocus: false
                        });
                    });
                    if(!isTemp) vscode.window.showInformationMessage(`✅ Relatório pronto!`);
                } else {
                    vscode.window.showWarningMessage(`O relatório não foi gerado. Resposta: ${stdout}`);
                }
                resolve();
            });
        });
    });
}

export function deactivate() {}