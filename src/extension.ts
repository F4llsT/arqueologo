import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
    
    let disposable = vscode.commands.registerCommand('arqueologo.analisarCodigo', (uri: vscode.Uri) => {
        
        // 1. Identifica o arquivo ou pasta clicada
        let targetPath = uri ? uri.fsPath : '';
        if (!targetPath) {
            vscode.window.showErrorMessage('Por favor, clique com o botão direito em um arquivo.');
            return;
        }

        // 2. Verifica se há um workspace aberto
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('Abra a pasta do seu projeto no VS Code primeiro.');
            return;
        }
        
        const workspaceRoot = workspaceFolders[0].uri.fsPath;

        // 3. PASSO MESTRE: Localiza o script Python DENTRO da pasta da extensão
        // Isso elimina a necessidade de copiar o arqueologo.py para a pasta do usuário
        const scriptPath = path.join(context.extensionPath, 'arqueologo.py');

        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage('Erro crítico: O motor "arqueologo.py" não foi encontrado dentro da extensão.');
            return;
        }

        // 4. Inicia a barra de progresso
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Arqueólogo: Analisando código com IA Local...",
            cancellable: false
        }, (progress) => {
            return new Promise<void>((resolve) => {
                
                // Monta o comando com aspas duplas para suportar caminhos com espaços no Linux
                const command = `python3 "${scriptPath}" "${targetPath}"`;
                
                // Executa o script Python
                exec(command, { cwd: workspaceRoot }, (error: Error | null, stdout: string, stderr: string) => {
                    if (error) {
                        vscode.window.showErrorMessage(`Erro na IA: ${error.message}`);
                        console.error(stderr);
                        resolve(); 
                        return;
                    }

                    // 5. LÓGICA DE ABERTURA AUTOMÁTICA
                    // O script Python gera o arquivo com o nome: [nome_do_arquivo]_doc.md
                    const fileName = path.basename(targetPath);
                    const reportName = `${fileName}_doc.md`;
                    const docPath = path.join(workspaceRoot, 'documentacao_gerada', reportName);

                    // Verifica se o relatório foi criado e abre ele ao lado (Beside)
                    if (fs.existsSync(docPath)) {
                        const openPath = vscode.Uri.file(docPath);
                        vscode.workspace.openTextDocument(openPath).then(doc => {
                            vscode.window.showTextDocument(doc, {
                                viewColumn: vscode.ViewColumn.Beside,
                                preserveFocus: false
                            });
                        });
                        vscode.window.showInformationMessage(`✅ Arqueólogo: Análise de "${fileName}" concluída!`);
                    } else {
                        vscode.window.showWarningMessage('Análise concluída, mas o arquivo de relatório não foi encontrado.');
                    }
                    
                    resolve();
                });
            });
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}