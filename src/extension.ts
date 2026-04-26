import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os'; // NOVO: Biblioteca para detectar o Sistema Operacional

export function activate(context: vscode.ExtensionContext) {
    
    let disposable = vscode.commands.registerCommand('arqueologo.analisarCodigo', async (uri: vscode.Uri) => {
        
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
            vscode.window.showErrorMessage('⚠️ Motor arqueologo.py não encontrado no pacote.');
            return;
        }

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "🏺 Arqueólogo: Analisando código localmente...",
            cancellable: false
        }, (progress) => {
            return new Promise<void>((resolve) => {
                
                // 🚀 LÓGICA MULTIPLATAFORMA (Windows vs Linux/Mac)
                // Se for win32 (Windows), usa 'python', senão usa 'python3'
                const pythonCmd = os.platform() === 'win32' ? 'python' : 'python3';
                
                // Monta o comando dinamicamente
                const command = `${pythonCmd} "${scriptPath}" "${targetPath}"`;
                
                exec(command, { cwd: workspaceRoot }, (error: Error | null, stdout: string, stderr: string) => {
                    if (error) {
                        vscode.window.showErrorMessage(`❌ Erro: ${stderr || error.message}`);
                        resolve(); 
                        return;
                    }

                    const targetName = path.basename(targetPath);
                    const reportName = `${targetName}_doc.md`;
                    const docPath = path.join(workspaceRoot, 'documentacao_gerada', reportName);

                    if (fs.existsSync(docPath)) {
                        const openPath = vscode.Uri.file(docPath);
                        vscode.workspace.openTextDocument(openPath).then(doc => {
                            vscode.window.showTextDocument(doc, {
                                viewColumn: vscode.ViewColumn.Beside,
                                preserveFocus: false
                            });
                        });
                        vscode.window.showInformationMessage(`✅ Relatório de "${targetName}" pronto!`);
                    } else {
                        // Exibe o que o Python retornou caso o relatório não apareça
                        vscode.window.showWarningMessage(`O relatório não foi gerado. Resposta da IA: ${stdout}`);
                    }
                    resolve();
                });
            });
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}