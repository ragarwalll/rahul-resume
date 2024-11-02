// scripts/build.js
const { execSync } = require('child_process');
const path = require('path');

// Change this to your main tex file name
const MAIN_TEX_FILE = 'resume.tex';

try {
    // First compilation
    console.log('First XeLaTeX pass...');
    execSync(`xelatex -interaction=nonstopmode ${MAIN_TEX_FILE}`, { stdio: 'inherit' });

    // Second compilation for references
    console.log('Second XeLaTeX pass for references...');
    execSync(`xelatex -interaction=nonstopmode ${MAIN_TEX_FILE}`, { stdio: 'inherit' });

    console.log('Successfully built document!');
} catch (error) {
    console.error('Error during compilation:', error.message);
    process.exit(1);
}