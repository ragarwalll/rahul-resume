const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const glob = require('glob');

// ANSI color codes
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    cyan: '\x1b[36m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m'
};

function findConfig(filename) {
    // Check workspace root (current directory)
    const workspaceConfig = path.join(process.cwd(), filename);
    if (fs.existsSync(workspaceConfig)) {
        console.log(`Using ${filename} from workspace: ${workspaceConfig}`);
        return workspaceConfig;
    }

    // Check user's home directory
    const homeConfig = path.join(os.homedir(), filename);
    if (fs.existsSync(homeConfig)) {
        console.log(`Using ${filename} from home directory: ${homeConfig}`);
        return homeConfig;
    }

    console.log(`No ${filename} found, will use default settings`);
    return null;
}

function colorDiff(output) {
    return output
        .replace(/^(@@ .+ @@)/gm, `${colors.cyan}$1${colors.reset}`)
        .replace(/^-.*$/gm, `${colors.red}$&${colors.reset}`)
        .replace(/^\+.*$/gm, `${colors.green}$&${colors.reset}`);
}

function formatFile(file, configPath) {
    console.log(`\nFormatting ${colors.cyan}${file}${colors.reset}...`);
    const configArgs = configPath ? ['-l', configPath] : [];
    const command = ['latexindent', '-kv', '-s', ...configArgs, file].join(' ');
    try {
        execSync(command, { stdio: ['inherit', 'pipe', 'inherit'] });
        console.log(`${colors.green}✓${colors.reset} Formatting completed`);
        return true;
    } catch (error) {
        if (error.stdout) {
            console.log(colorDiff(error.stdout.toString()));
        }
        console.error(`${colors.red}✗${colors.reset} Formatting failed`);
        return false;
    }
}

function lintFile(file, configPath) {
    console.log(`\nLinting ${colors.cyan}${file}${colors.reset}...`);
    try {
        const configArgs = configPath ? ['-l', configPath] : [];
        const command = ['chktex', ...configArgs, file].join(' ');
        const output = execSync(command, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });

        if (output.trim()) {
            console.log(`${colors.yellow}⚠${colors.reset} Linting issues found:`);
            const formattedOutput = output.split('\n')
                .filter(line => line.trim())
                .map(line => {
                    if (line.includes('Warning')) {
                        return `${colors.yellow}${line}${colors.reset}`;
                    } else if (line.includes('Error')) {
                        return `${colors.red}${line}${colors.reset}`;
                    }
                    return line;
                })
                .join('\n');
            console.log(formattedOutput);
            return false;
        } else {
            console.log(`${colors.green}✓${colors.reset} No linting issues found`);
            return true;
        }
    } catch (error) {
        if (error.status === 1 && error.stdout) {
            console.log(`${colors.yellow}⚠${colors.reset} Linting issues found:`);
            console.log(error.stdout.toString());
            return false;
        } else {
            console.error(`${colors.red}✗${colors.reset} Linting failed with error:`);
            console.error(error.message);
            return false;
        }
    }
}

async function processFiles() {
    let hasErrors = false;
    const stats = {
        total: 0,
        formatted: 0,
        linted: 0,
        formatErrors: 0,
        lintErrors: 0
    };

    try {
        // Find configuration files
        const latexindentConfig = findConfig('latexindent.yaml');
        const chktexConfig = findConfig('.chktexrc');

        // Find all .tex and .cls files
        const texFiles = glob.sync('**/*.{tex,cls}', {
            ignore: [
                'node_modules/**',
                'build/**',
                'dist/**',
                '_minted-*/**',
                '**/python-data.tex'
            ]
        });

        if (texFiles.length === 0) {
            console.log('No .tex or .cls files found');
            return process.exit(0);
        }

        stats.total = texFiles.length;
        console.log(`\nFound ${texFiles.length} files to process`);

        // First run: Format all files
        console.log('\n=== Running Formatter ===');
        for (const file of texFiles) {
            const formatSuccess = formatFile(file, latexindentConfig);
            if (formatSuccess) {
                stats.formatted++;
            } else {
                stats.formatErrors++;
                hasErrors = true;
            }
        }

        // Second run: Lint all files
        if (chktexConfig) {
            console.log('\n=== Running Linter ===');
            for (const file of texFiles) {
                const lintSuccess = lintFile(file, chktexConfig);
                if (lintSuccess) {
                    stats.linted++;
                } else {
                    stats.lintErrors++;
                    hasErrors = true;
                }
            }
        } else {
            console.log('\n=== Skipping Linter (no .chktexrc found) ===');
        }

        // Print summary
        console.log('\n' + '='.repeat(50));
        console.log('Summary:');
        console.log('-'.repeat(50));
        console.log(`Total files processed: ${stats.total}`);
        console.log(`Successfully formatted: ${stats.formatted}/${stats.total}`);
        if (chktexConfig) {
            console.log(`Successfully linted: ${stats.linted}/${stats.total}`);
            console.log(`Lint errors: ${stats.lintErrors}`);
        }
        console.log(`Format errors: ${stats.formatErrors}`);
        console.log('='.repeat(50));

        process.exit(hasErrors ? 1 : 0);
    } catch (error) {
        console.error('Error processing files:', error.message);
        process.exit(1);
    }
}

// Run the script
processFiles().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
});