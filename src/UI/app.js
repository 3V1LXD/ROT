const fileInputIds = {
    config: 'config-file-input',
    bindings: 'bindings-file-input',
    rotations: 'rotations-file-input'
};

const fileContentIds = {
    config: 'config-file-content',
    bindings: 'bindings-file-content',
    rotations: 'rotations-file-content'
};

const saveBtnIds = {
    config: 'config-save-btn',
    bindings: 'bindings-save-btn',
    rotations: 'rotations-save-btn'
};

const loadedFiles = {
    config: null,
    bindings: null,
    rotations: null
};

// Helper function to read file and display content
// function handleFileInput(event, type) {
//     const file = event.target.files[0];
//     loadedFiles[type] = file;
//     const reader = new FileReader();
//     reader.onload = (e) => {
//         const data = e.target.result;
//         const iniData = parseINI(data);
//         document.getElementById(fileContentIds[type]).textContent = JSON.stringify(iniData, null, 2);
//     };
//     reader.readAsText(file);
// }
function handleFileInput(event, type) {
    const file = event.target.files[0];
    loadedFiles[type] = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = e.target.result;
        const iniData = parseINI(data);
        const contentContainer = document.getElementById(fileContentIds[type]);
        const form = createFormFromData(iniData);
        contentContainer.innerHTML = '';
        contentContainer.appendChild(form);
    };
    reader.readAsText(file);
}

function createFormFromData(data) {
    const form = document.createElement('form');
    for (const sectionName in data) {
        const section = data[sectionName];
        const sectionHeader = document.createElement('h4');
        sectionHeader.textContent = `[${sectionName}]`;
        form.appendChild(sectionHeader);
        for (const key in section) {
            const inputWrapper = document.createElement('div');
            inputWrapper.classList.add('mb-3');
            const label = document.createElement('label');
            label.classList.add('form-label');
            label.textContent = key;
            const input = document.createElement('input');
            input.classList.add('form-control');
            input.value = section[key];
            input.setAttribute('data-section', sectionName);
            input.setAttribute('data-key', key);
            inputWrapper.appendChild(label);
            inputWrapper.appendChild(input);
            form.appendChild(inputWrapper);
        }
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.classList.add('btn', 'btn-primary');
        submitButton.textContent = 'Save Changes';
        form.appendChild(submitButton);
    }
    form.addEventListener('submit', handleFormSubmit);
    return form;
}

function handleFormSubmit(event) {
    event.preventDefault();
    alert('Form submitted');
    const formData = new FormData(event.target);
    const newContent = formDataToINI(formData);
    const type = formData.get('type');
    const filename = loadedFiles[type].name;
    const blob = new Blob([newContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, 100);
}

function formDataToINI(formData) {
    const sections = new Map();
    for (const [key, value] of formData.entries()) {
        const [, section, keyName] = key.match(/^(\w+)\[(\w+)\]$/);
        if (!sections.has(section)) {
            sections.set(section, new Map());
        }
        sections.get(section).set(keyName, value);
    }
    let iniText = '';
    for (const [sectionName, section] of sections.entries()) {
        iniText += `[${sectionName}]\n`;
        for (const [key, value] of section.entries()) {
            iniText += `${key} = ${value}\n`;
        }
        iniText += '\n';
    }
    return iniText;
}

// Helper function to save changes
// function handleSaveBtn(type) {
//     if (!loadedFiles[type]) {
//         alert('No file loaded');
//         return;
//     }
//     const form = document.getElementById(fileContentIds[type]).querySelector('form');
//     const formData = new FormData(form);
//     const iniContent = formDataToINI(formData);

//     for (const [section, values] of Object.entries(iniData)) {
//         iniContent += `[${section}]\n`;
//         for (const [key, value] of Object.entries(values)) {
//             iniContent += `${key} = ${value}\n`;
//         }
//         iniContent += '\n';
//     }

//     const blob = new Blob([iniContent], { type: 'text/plain' });
//     const url = URL.createObjectURL(blob);

//     const link = document.createElement('a');
//     link.href = url;
//     link.download = loadedFiles[type].name;
//     link.style.display = 'none';
//     document.body.appendChild(link);
//     link.click();
//     setTimeout(() => {
//         document.body.removeChild(link);
//         URL.revokeObjectURL(url);
//     }, 100);
// }
function handleSaveBtn(type) {
    if (!loadedFiles[type]) {
        alert('No file loaded');
        return;
    }
    const form = document.getElementById(fileContentIds[type]).querySelector('form');
    const formData = new FormData(form);
    const iniContent = formDataToINI(formData);

    const iniData = parseINI(iniContent);

    let iniText = '';
    for (const [section, values] of Object.entries(iniData)) {
        iniText += `[${section}]\n`;
        for (const [key, value] of Object.entries(values)) {
            iniText += `${key} = ${value}\n`;
        }
        iniText += '\n';
    }

    const blob = new Blob([iniText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = loadedFiles[type].name;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    setTimeout(() => {
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, 100);
}


// Bind events for each tab
for (const type of Object.keys(fileInputIds)) {
    document.getElementById(fileInputIds[type]).addEventListener('change', (event) => handleFileInput(event, type));
    document.getElementById(saveBtnIds[type]).addEventListener('click', () => handleSaveBtn(type));
}

function parseINI(data) {
    const lines = data.split(/\r\n|\n|\r/);
    let result = {};
    let section = null;

    lines.forEach((line) => {
        line = line.trim();
        if (line.startsWith(';') || line === '') {
            return;
        }
        if (line.startsWith('[') && line.endsWith(']')) {
            section = line.slice(1, -1);
            result[section] = {};
        } else {
            const [key, value] = line.split('=', 2);
            if (section) {
                result[section][key.trim()] = value.trim();
            }
        }
    });

    return result;
}