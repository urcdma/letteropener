const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process'); // 使用spawn代替exec
const astBuilder = require('./js_parser/astBuilder.js');

function createWindow() {
    let win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        }
    });

    win.loadFile('index.html');
}

app.on('ready', createWindow);

ipcMain.on('upload-code', (event, code) => {
    const validationScript = spawn('python', ['path_to_validation_script.py']);
    let stdoutData = '';

    validationScript.stdout.on('data', (data) => {
        stdoutData += data.toString();
    });

    validationScript.stderr.on('data', (data) => {
        console.error(`Validation script error: ${data}`);
    });

    validationScript.on('close', (code) => {
        if (stdoutData.includes("Valid")) {
            event.reply('code-validation-result', { isValid: true });
        } else {
            event.reply('code-validation-result', { isValid: false });
        }
    });

    validationScript.stdin.write(code);
    validationScript.stdin.end();
});

ipcMain.on('parse-code', (event, code) => {
    const parserScript = spawn('python', ['code_parser_script.py']);
    let stdoutData = '';

    parserScript.stdout.on('data', (data) => {
        stdoutData += data.toString();
    });

    parserScript.stderr.on('data', (data) => {
        console.error(`Parsing script error: ${data}`);
    });

    parserScript.on('close', (code) => {
        try {
            const parseResult = JSON.parse(stdoutData);
            event.reply('code-parse-result', { success: true, data: parseResult });
        } catch (e) {
            console.error("Error parsing the output from code_parser_script.py:", e);
            event.reply('code-parse-result', { success: false });
        }
    });

    parserScript.stdin.write(code);
    parserScript.stdin.end();
});

// New event listener for JavaScript code parsing
ipcMain.on('upload-js-code', (event, code) => {
    try {
        const jsAST = astBuilder.parse(code);
        event.reply('js-code-parse-result', { success: true, data: jsAST });
    } catch (e) {
        console.error("Error parsing JavaScript:", e);
        event.reply('js-code-parse-result', { success: false });
    }
});


/*
ipcMain.on('toMain', (event, data) => {
    // TODO: Handle the data and perform necessary actions for toMain
    console.log(`Received data from renderer for channel toMain:`, data);
});

ipcMain.on('uploadFile', (event, data) => {
    // TODO: Handle the data and perform necessary actions for uploadFile
    console.log(`Received data from renderer for channel uploadFile:`, data);
});

ipcMain.on('pasteCode', (event, data) => {
    // TODO: Handle the data and perform necessary actions for pasteCode
    console.log(`Received data from renderer for channel pasteCode:`, data);
});

ipcMain.on('validateCode', (event, data) => {
    // TODO: Handle the data and perform necessary actions for validateCode
    console.log(`Received data from renderer for channel validateCode:`, data);
});

ipcMain.on('parseCode', (event, data) => {
    // TODO: Handle the data and perform necessary actions for parseCode
    console.log(`Received data from renderer for channel parseCode:`, data);
});
*/