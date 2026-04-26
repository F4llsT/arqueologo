import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    
    let disposable = vscode.commands.registerCommand('arqueologo.analisarCodigo', (uri: vscode.Uri) => {
        
        let targetPath = uri ? uri.fsPath : '';
        if (!targetPath) {
            vscode.window.showErrorMessage('Por favor, clique com o botão direito em um arquivo.');
            return;
        }

        const isDirectory = fs.statSync(targetPath).isDirectory();
        const targetDir = isDirectory ? targetPath : path.dirname(targetPath);

        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('Abra a pasta do seu projeto no VS Code primeiro.');
            return;
        }
        
        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const scriptPath = path.join(workspaceRoot, 'arqueologo.py');

        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage('O arquivo arqueologo.py não foi encontrado na raiz do projeto.');
            return;
        }

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Arqueólogo: Analisando código com IA Local...",
            cancellable: false
        }, (progress) => {
            return new Promise<void>((resolve) => {
                
                const command = `python3 "${scriptPath}" "${targetDir}"`;
                
                // CORREÇÃO: Adicionamos os tipos explícitos (Error | null, string, string) para agradar o TypeScript
                exec(command, { cwd: workspaceRoot }, (error: Error | null, stdout: string, stderr: string) => {
                    if (error) {
                        vscode.window.showErrorMessage(`Erro na IA: ${error.message}`);
                        console.error(stderr);
                        resolve(); 
                        return;
                    }

                    const fileName = path.basename(targetDir);
                    const docPath = path.join(workspaceRoot, 'documentacao_gerada', `${fileName}_documentacao.md`);

                    if(fs.existsSync(docPath)) {
                        const openPath = vscode.Uri.file(docPath);
                        vscode.workspace.openTextDocument(openPath).then(doc => {
                            vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
                        });
                    }
                    vscode.window.showInformationMessage('✅ Análise do Arqueólogo concluída! Verifique a pasta documentacao_gerada.');
                    resolve();
                });
            });
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}