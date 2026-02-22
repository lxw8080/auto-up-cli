#!/usr/bin/env node

/**
 * AI CLI工具管理器 v1.2.1
 * 统一管理AI CLI工具的安装和升级
 *
 * 主要特性:
 * - 支持17+AI CLI工具
 * - 交互式菜单和命令行模式
 * - 快速模式和验证模式切换
 * - 跨平台支持 (Windows/macOS/Linux)
 */

const { execSync, exec } = require('child_process');
const readline = require('readline');
const chalk = require('chalk');

// 配置要管理的CLI工具
const CLI_TOOLS = {
  // 主流AI助手
  'gemini-cli': {
    name: 'gemini-cli',
    package: '@google/gemini-cli',
    displayName: 'Gemini CLI',
    category: 'AI助手'
  },
  'claude-code': {
    name: 'claude-code',
    package: '@anthropic-ai/claude-code',
    displayName: 'Claude Code',
    category: 'AI助手',
    installCommands: {
      windows: 'powershell -ExecutionPolicy Bypass -Command "irm https://claude.ai/install.ps1 | iex"',
      macos: 'curl -fsSL https://claude.ai/install.sh | bash',
      linux: 'curl -fsSL https://claude.ai/install.sh | bash'
    }
  },
  'codex': {
    name: 'codex',
    package: '@openai/codex',
    displayName: 'Codex CLI',
    category: 'AI助手'
  },
  'auggie': {
    name: 'auggie',
    package: '@augmentcode/auggie',
    displayName: 'Auggie CLI',
    category: 'AI助手'
  },
  // GitHub官方AI工具
  'copilot-cli': {
    name: 'copilot-cli',
    package: '@github/copilot',
    displayName: 'GitHub Copilot CLI',
    category: 'AI助手',
    note: '需要GitHub Copilot订阅'
  },
  // AI编程助手
  'continue': {
    name: 'continue',
    package: '@continuedev/cli',
    displayName: 'Continue CLI',
    category: 'AI编程助手'
  },
  // CodeGPT 实际是Go语言编写的二进制，npm包不存在
  // 'codegpt': {
  //   name: 'codegpt',
  //   package: 'codegpt-cli',
  //   displayName: 'CodeGPT CLI',
  //   category: 'AI编程助手'
  // },
  // Tabnine CLI 不存在npm包，只有IDE插件
  // 'tabnine': {
  //   name: 'tabnine',
  //   package: '@tabnine/cli',
  //   displayName: 'Tabnine CLI',
  //   category: 'AI编程助手'
  // },
  'opencommit': {
    name: 'opencommit',
    package: 'opencommit',
    displayName: 'OpenCommit',
    category: 'AI编程助手'
  },
  // Aider 是Python包，不是npm包
  // 'aider': {
  //   name: 'aider',
  //   package: 'aider-chat',
  //   displayName: 'Aider',
  //   category: 'AI编程助手'
  // },
  'gitleaks': {
    name: 'gitleaks',
    package: 'gitleaks',
    displayName: 'GitLeaks',
    category: '代码安全'
  },
  'gitmoji-cli': {
    name: 'gitmoji-cli',
    package: 'gitmoji-cli',
    displayName: 'Gitmoji CLI',
    category: 'Git工具'
  },
  // 通义千问系列 (包不存在)
  // 'qwen-code': {
  //   name: 'qwen-code',
  //   package: 'qwen2.5-coder',
  //   displayName: 'Qwen2.5 Coder',
  //   category: 'AI编程助手',
  //   note: '需要确认包名'
  // },
  // 预留更多工具位置
  // 'kilo-code': {
  //   name: 'kilo-code',
  //   package: 'kilo-code-cli',
  //   displayName: 'Kilo Code CLI',
  //   category: 'AI编程助手',
  //   note: '需要确认包名'
  // },
  'iflow': {
    name: 'iflow',
    package: '@iflow-ai/iflow-cli',
    displayName: 'iFlow CLI',
    category: 'AI助手'
  },
  'opencode': {
    name: 'opencode',
    package: 'opencode-ai',
    displayName: 'OpenCode',
    category: 'AI编程助手'
  },
  'grok-cli': {
    name: 'grok-cli',
    package: '@vibe-kit/grok-cli',
    displayName: 'Grok CLI',
    category: 'AI助手'
  },
  'qoder': {
    name: 'qoder',
    package: '@qoder-ai/qodercli',
    displayName: 'Qoder',
    category: 'AI编程助手'
  },
  // 新增辅助工具
  'openspec': {
    name: 'openspec',
    package: '@fission-ai/openspec',
    displayName: 'OpenSpec',
    category: 'AI开发工具',
    note: 'AI-native system for spec-driven development'
  },
  'commitizen': {
    name: 'commitizen',
    package: 'commitizen',
    displayName: 'Commitizen',
    category: 'Git工具',
    note: '规范化Git提交信息的工具'
  },
  'conventional-changelog-cli': {
    name: 'conventional-changelog-cli',
    package: 'conventional-changelog-cli',
    displayName: 'Conventional Changelog',
    category: 'Git工具',
    note: '基于约定式提交生成changelog'
  },
  'semantic-release-cli': {
    name: 'semantic-release-cli',
    package: 'semantic-release-cli',
    displayName: 'Semantic Release',
    category: 'Git工具',
    note: '自动化版本管理和发布'
  },
  'release-it': {
    name: 'release-it',
    package: 'release-it',
    displayName: 'Release It',
    category: 'Git工具',
    note: '交互式发布工具'
  },
  'np': {
    name: 'np',
    package: 'np',
    displayName: 'NP',
    category: 'Git工具',
    note: '更好的npm发布体验'
  },
  'auto-changelog': {
    name: 'auto-changelog',
    package: 'auto-changelog',
    displayName: 'Auto Changelog',
    category: 'Git工具',
    note: '自动生成changelog'
  },
  'standard-version': {
    name: 'standard-version',
    package: 'standard-version',
    displayName: 'Standard Version',
    category: 'Git工具',
    note: '基于约定式提交自动版本管理'
  },
  'changeset': {
    name: 'changeset',
    package: '@changesets/cli',
    displayName: 'Changesets',
    category: 'Git工具',
    note: 'Monorepo版本管理工具'
  },
  'husky': {
    name: 'husky',
    package: 'husky',
    displayName: 'Husky',
    category: 'Git工具',
    note: 'Git钩子管理工具'
  },
  'lint-staged': {
    name: 'lint-staged',
    package: 'lint-staged',
    displayName: 'Lint Staged',
    category: '代码质量',
    note: '只对暂存文件运行linter'
  },
  'prettier': {
    name: 'prettier',
    package: 'prettier',
    displayName: 'Prettier',
    category: '代码质量',
    note: '代码格式化工具'
  },
  'eslint': {
    name: 'eslint',
    package: 'eslint',
    displayName: 'ESLint',
    category: '代码质量',
    note: 'JavaScript代码检查工具'
  },
  'typescript': {
    name: 'typescript',
    package: 'typescript',
    displayName: 'TypeScript',
    category: '代码质量',
    note: 'JavaScript的超集，添加类型系统'
  },
  'nodemon': {
    name: 'nodemon',
    package: 'nodemon',
    displayName: 'Nodemon',
    category: '开发工具',
    note: 'Node.js应用自动重启工具'
  },
  'pm2': {
    name: 'pm2',
    package: 'pm2',
    displayName: 'PM2',
    category: '开发工具',
    note: 'Node.js进程管理器'
  },
  'forever': {
    name: 'forever',
    package: 'forever',
    displayName: 'Forever',
    category: '开发工具',
    note: 'Node.js进程守护工具'
  },
  'cross-env': {
    name: 'cross-env',
    package: 'cross-env',
    displayName: 'Cross Env',
    category: '开发工具',
    note: '跨平台环境变量设置'
  },
  'rimraf': {
    name: 'rimraf',
    package: 'rimraf',
    displayName: 'Rimraf',
    category: '开发工具',
    note: '跨平台文件删除工具'
  },
  'mkdirp': {
    name: 'mkdirp',
    package: 'mkdirp',
    displayName: 'Mkdirp',
    category: '开发工具',
    note: '递归创建目录'
  },
  'ncp': {
    name: 'ncp',
    package: 'ncp',
    displayName: 'NCP',
    category: '开发工具',
    note: '异步文件复制'
  },
  'http-server': {
    name: 'http-server',
    package: 'http-server',
    displayName: 'HTTP Server',
    category: '开发工具',
    note: '简单的HTTP服务器'
  },
  'serve': {
    name: 'serve',
    package: 'serve',
    displayName: 'Serve',
    category: '开发工具',
    note: '静态文件服务器'
  },
  'live-server': {
    name: 'live-server',
    package: 'live-server',
    displayName: 'Live Server',
    category: '开发工具',
    note: '带实时重载的开发服务器'
  },
  'webpack-cli': {
    name: 'webpack-cli',
    package: 'webpack-cli',
    displayName: 'Webpack CLI',
    category: '构建工具',
    note: 'Webpack命令行工具'
  },
  'vite': {
    name: 'vite',
    package: 'vite',
    displayName: 'Vite',
    category: '构建工具',
    note: '下一代前端构建工具'
  },
  'parcel': {
    name: 'parcel',
    package: 'parcel',
    displayName: 'Parcel',
    category: '构建工具',
    note: '零配置构建工具'
  },
  'rollup': {
    name: 'rollup',
    package: 'rollup',
    displayName: 'Rollup',
    category: '构建工具',
    note: 'JavaScript模块打包器'
  },
  'esbuild': {
    name: 'esbuild',
    package: 'esbuild',
    displayName: 'ESBuild',
    category: '构建工具',
    note: '极速JavaScript打包器'
  },
  'swc': {
    name: 'swc',
    package: '@swc/cli',
    displayName: 'SWC',
    category: '构建工具',
    note: 'Rust编写的超快JavaScript编译器'
  },
  'babel-cli': {
    name: 'babel-cli',
    package: '@babel/cli',
    displayName: 'Babel CLI',
    category: '构建工具',
    note: 'JavaScript编译器'
  },
  'ts-node': {
    name: 'ts-node',
    package: 'ts-node',
    displayName: 'TS Node',
    category: '构建工具',
    note: 'TypeScript执行环境'
  },
  'tsx': {
    name: 'tsx',
    package: 'tsx',
    displayName: 'TSX',
    category: '构建工具',
    note: 'TypeScript执行器（更快的ts-node替代品）'
  },
  'jest': {
    name: 'jest',
    package: 'jest',
    displayName: 'Jest',
    category: '测试工具',
    note: 'JavaScript测试框架'
  },
  'vitest': {
    name: 'vitest',
    package: 'vitest',
    displayName: 'Vitest',
    category: '测试工具',
    note: '极速单元测试框架'
  },
  'mocha': {
    name: 'mocha',
    package: 'mocha',
    displayName: 'Mocha',
    category: '测试工具',
    note: 'JavaScript测试框架'
  },
  'cypress': {
    name: 'cypress',
    package: 'cypress',
    displayName: 'Cypress',
    category: '测试工具',
    note: '端到端测试框架'
  },
  'playwright': {
    name: 'playwright',
    package: 'playwright',
    displayName: 'Playwright',
    category: '测试工具',
    note: '现代端到端测试工具'
  },
  'ava': {
    name: 'ava',
    package: 'ava',
    displayName: 'AVA',
    category: '测试工具',
    note: '未来的测试运行器'
  },
  'tap': {
    name: 'tap',
    package: 'tap',
    displayName: 'TAP',
    category: '测试工具',
    note: '测试任何协议'
  },
  'supertest': {
    name: 'supertest',
    package: 'supertest',
    displayName: 'Supertest',
    category: '测试工具',
    note: 'HTTP断言库'
  },
  'nyc': {
    name: 'nyc',
    package: 'nyc',
    displayName: 'NYC',
    category: '测试工具',
    note: '代码覆盖率工具'
  },
  'codecov': {
    name: 'codecov',
    package: 'codecov',
    displayName: 'Codecov',
    category: '测试工具',
    note: '代码覆盖率报告'
  },
  'nock': {
    name: 'nock',
    package: 'nock',
    displayName: 'Nock',
    category: '测试工具',
    note: 'HTTP服务器模拟'
  },
  'sinon': {
    name: 'sinon',
    package: 'sinon',
    displayName: 'Sinon',
    category: '测试工具',
    note: '测试间谍、存根和模拟'
  },
  'chai': {
    name: 'chai',
    package: 'chai',
    displayName: 'Chai',
    category: '测试工具',
    note: 'BDD/TDD断言库'
  },
  'expect': {
    name: 'expect',
    package: 'expect',
    displayName: 'Expect',
    category: '测试工具',
    note: 'Jest的断言库'
  },
  'puppeteer': {
    name: 'puppeteer',
    package: 'puppeteer',
    displayName: 'Puppeteer',
    category: '测试工具',
    note: '无头Chrome Node.js API'
  },
  'selenium-webdriver': {
    name: 'selenium-webdriver',
    package: 'selenium-webdriver',
    displayName: 'Selenium WebDriver',
    category: '测试工具',
    note: '浏览器自动化工具'
  },
  'webdriverio': {
    name: 'webdriverio',
    package: 'webdriverio',
    displayName: 'WebdriverIO',
    category: '测试工具',
    note: '下一代浏览器和移动端自动化测试框架'
  }
};

// 颜色定义
const colors = {
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m'
};

// 获取已安装版本
function getInstalledVersion(packageName) {
  try {
    const result = execSync(`npm list -g ${packageName} --depth=0 --json`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    const data = JSON.parse(result);
    if (data.dependencies && data.dependencies[packageName]) {
      return data.dependencies[packageName].version;
    }
    return null;
  } catch (error) {
    return null;
  }
}

// 获取npm最新版本
function getLatestVersion(packageName) {
  try {
    const result = execSync(`npm view ${packageName} version`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return result.trim();
  } catch (error) {
    return null;
  }
}

// 安装或升级包
function installPackage(packageName, displayName, currentVersion) {
  console.log(`\n${colors.cyan}正在安装/升级 ${displayName}...${colors.reset}`);

  try {
    if (currentVersion) {
      console.log(`${colors.yellow}当前版本:${colors.reset} ${currentVersion}`);
    }

    execSync(`npm install -g ${packageName}`, {
      stdio: 'inherit'
    });

    const newVersion = getInstalledVersion(packageName);
    console.log(`${colors.green}✓ ${displayName} 安装完成${colors.reset}`);
    console.log(`${colors.green}✓ 新版本:${colors.reset} ${newVersion}`);

    return {
      success: true,
      newVersion,
      upgraded: currentVersion !== newVersion
    };
  } catch (error) {
    console.error(`${colors.red}✗ ${displayName} 安装失败${colors.reset}`);
    console.error(error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

// 获取平台特定的自定义安装命令
function getPlatformInstallCommand(tool) {
  if (!tool.installCommands) return null;

  const platform = process.platform;
  let cmd = null;

  if (platform === 'win32') {
    cmd = tool.installCommands.windows || null;
  } else if (platform === 'darwin') {
    cmd = tool.installCommands.macos || null;
  } else {
    cmd = tool.installCommands.linux || null;
  }

  return cmd;
}

// 安装或升级包（支持自定义安装命令）
function installWithCommand(packageName, displayName, currentVersion, customCmd) {
  console.log(`\n${colors.cyan}正在安装/升级 ${displayName}...${colors.reset}`);

  try {
    if (currentVersion) {
      console.log(`${colors.yellow}当前版本:${colors.reset} ${currentVersion}`);
    }

    if (customCmd) {
      console.log(`${colors.cyan}使用自定义安装命令...${colors.reset}`);
      execSync(customCmd, { stdio: 'inherit', shell: true });
    } else {
      execSync(`npm install -g ${packageName}`, { stdio: 'inherit' });
    }

    const newVersion = getInstalledVersion(packageName) || 'unknown';
    console.log(`${colors.green}✓ ${displayName} 安装完成${colors.reset}`);
    console.log(`${colors.green}✓ 新版本:${colors.reset} ${newVersion}`);

    return {
      success: true,
      newVersion,
      upgraded: currentVersion !== newVersion
    };
  } catch (error) {
    // 自定义命令失败，尝试npm作为后备
    if (customCmd && !customCmd.includes('npm install')) {
      console.log(`${colors.yellow}自定义安装失败，尝试npm安装...${colors.reset}`);
      try {
        execSync(`npm install -g ${packageName}`, { stdio: 'inherit' });
        const newVersion = getInstalledVersion(packageName) || 'unknown';
        console.log(`${colors.green}✓ ${displayName} 安装完成${colors.reset}`);
        return {
          success: true,
          newVersion,
          upgraded: currentVersion !== newVersion
        };
      } catch (npmError) {
        console.error(`${colors.red}✗ ${displayName} 安装失败${colors.reset}`);
        return { success: false, error: npmError.message };
      }
    }
    console.error(`${colors.red}✗ ${displayName} 安装失败${colors.reset}`);
    return { success: false, error: error.message };
  }
}

// 检查单个工具
function checkTool(toolKey, tool) {
  console.log(`\n${colors.bright}检查 ${tool.displayName}...${colors.reset}`);

  const currentVersion = getInstalledVersion(tool.package);
  const latestVersion = getLatestVersion(tool.package);
  const customCmd = getPlatformInstallCommand(tool);

  if (!currentVersion) {
    console.log(`${colors.yellow}未安装${colors.reset}`);
    return installWithCommand(tool.package, tool.displayName, null, customCmd);
  } else {
    console.log(`${colors.green}已安装${colors.reset} - 当前版本: ${currentVersion}`);

    if (latestVersion && currentVersion !== latestVersion) {
      console.log(`${colors.yellow}发现新版本: ${latestVersion}${colors.reset}`);
      return installWithCommand(tool.package, tool.displayName, currentVersion, customCmd);
    } else {
      console.log(`${colors.green}已是最新版本${colors.reset}`);
      return {
        success: true,
        currentVersion,
        isLatest: true
      };
    }
  }
}

// 检查所有工具
function checkAllTools() {
  console.log(`${colors.bright}${colors.cyan}
╔════════════════════════════════════════╗
║        AI CLI 工具管理器 v1.2.1         ║
║                                        ║
║  管理: 17+ AI编程CLI工具               ║
║                                        ║
╚════════════════════════════════════════╝
${colors.reset}`);

  const results = {};

  for (const [key, tool] of Object.entries(CLI_TOOLS)) {
    results[key] = checkTool(key, tool);
  }

  // 总结报告
  console.log(`\n${colors.bright}═══════════════════════════════════════${colors.reset}`);
  console.log(`${colors.bright}升级总结${colors.reset}`);
  console.log(`${colors.bright}═══════════════════════════════════════${colors.reset}\n`);

  let upgradeCount = 0;
  let installCount = 0;
  let latestCount = 0;

  for (const [key, result] of Object.entries(results)) {
    const tool = CLI_TOOLS[key];

    if (result.success) {
      if (result.isLatest) {
        latestCount++;
        console.log(`${colors.green}✓${colors.reset} ${tool.displayName}: 已是最新版本 (${result.currentVersion})`);
      } else if (result.upgraded) {
        upgradeCount++;
        console.log(`${colors.green}↑${colors.reset} ${tool.displayName}: 已升级到 ${result.newVersion}`);
      } else if (!result.currentVersion) {
        installCount++;
        console.log(`${colors.green}↓${colors.reset} ${tool.displayName}: 已安装 ${result.newVersion}`);
      }
    } else {
      console.log(`${colors.red}✗${colors.reset} ${tool.displayName}: 安装失败`);
    }
  }

  console.log(`\n${colors.bright}统计:${colors.reset}`);
  console.log(`  ${colors.green}新安装:${colors.reset} ${installCount}`);
  console.log(`  ${colors.green}已升级:${colors.reset} ${upgradeCount}`);
  console.log(`  ${colors.green}已是最新:${colors.reset} ${latestCount}`);
  console.log(`  ${colors.bright}总计:${colors.reset} ${Object.keys(CLI_TOOLS).length}\n`);
}

// 检查单个工具
function checkSingleTool(toolName) {
  const toolKey = Object.keys(CLI_TOOLS).find(
    key => key === toolName || CLI_TOOLS[key].name === toolName || CLI_TOOLS[key].package === toolName
  );

  if (!toolKey) {
    console.error(`${colors.red}错误: 找不到工具 "${toolName}"${colors.reset}`);
    console.log(`\n支持的工具: ${Object.keys(CLI_TOOLS).join(', ')}`);
    process.exit(1);
  }

  checkTool(toolKey, CLI_TOOLS[toolKey]);
}

// 显示主菜单
function showMainMenu() {
  console.log(`\n${colors.bright}${colors.cyan}
╔══════════════════════════════════════════════════════════╗
║              AI CLI 工具管理器 v1.2.1                     ║
║                                                          ║
║  请选择操作模式:                                         ║
║                                                          ║
║  [1] 交互式选择工具（推荐）                               ║
║  [2] 全部升级（自动检测并升级所有工具）                   ║
║  [3] 查看所有工具状态                                     ║
║  [0] 退出                                                ║
╚══════════════════════════════════════════════════════════╝
${colors.reset}\n`);
}

// 交互式工具选择菜单
function showToolSelectionMenu(selectedTools = new Set(), verifyVersions = false) {
  console.log(`\n${colors.bright}═══════════════════════════════════════════${colors.reset}`);
  console.log(`${colors.bright}选择要安装/升级的工具${colors.reset}`);
  console.log(`${colors.bright}═══════════════════════════════════════════${colors.reset}\n`);

  // 按类别分组工具
  const toolsByCategory = {};
  for (const [key, tool] of Object.entries(CLI_TOOLS)) {
    const category = tool.category || '其他';
    if (!toolsByCategory[category]) {
      toolsByCategory[category] = [];
    }
    toolsByCategory[category].push({ key, tool });
  }

  // 创建显示顺序到工具键的映射
  const displayOrderToKey = [];
  let index = 1;
  for (const [category, tools] of Object.entries(toolsByCategory)) {
    console.log(`\n${colors.cyan}━━━ ${category} ━━━${colors.reset}`);

    for (const { key, tool } of tools) {
      const isSelected = selectedTools.has(key);

      let status = '';
      if (verifyVersions) {
        const currentVersion = getInstalledVersion(tool.package);
        const latestVersion = getLatestVersion(tool.package);

        if (!currentVersion) {
          status = `${colors.red}[未安装]${colors.reset}`;
        } else if (latestVersion && currentVersion !== latestVersion) {
          status = `${colors.yellow}[v${currentVersion} → v${latestVersion}]${colors.reset}`;
        } else {
          status = `${colors.green}[v${currentVersion} 已是最新]${colors.reset}`;
        }
      } else {
        status = `${colors.dim}[点击查看状态]${colors.reset}`;
      }

      const marker = isSelected ? `${colors.green}✓${colors.reset}` : ' ';
      const note = tool.note ? ` ${colors.dim}(${tool.note})${colors.reset}` : '';
      console.log(`  ${marker} [${index}] ${colors.cyan}${tool.displayName}${colors.reset} ${status}${note}`);

      // 存储映射关系
      displayOrderToKey[index - 1] = key;
      index++;
    }
  }

  // 存储映射关系到全局变量或函数闭包
  if (typeof global !== 'undefined') {
    global.displayOrderToKey = displayOrderToKey;
  } else {
    // 如果是在浏览器环境或其他环境，使用函数属性存储
    showToolSelectionMenu.displayOrderToKey = displayOrderToKey;
  }

  console.log(`\n${colors.bright}操作:${colors.reset}`);
  console.log(`  [空格] 选择/取消 | [回车] 确认选择 | [A] 全选 | [N] 全不选 | [Q] 返回`);
  if (!verifyVersions) {
    console.log(`  [C] 验证工具状态（显示安装版本）`);
  } else {
    console.log(`  [C] 隐藏工具状态（快速显示）`);
  }
}

// 交互式模式
function interactiveMode() {
  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const selectedTools = new Set();
    let currentView = 'main'; // 'main' or 'tools'
    let verifyVersions = false; // 控制是否验证工具状态

    function displayMainMenu() {
      showMainMenu();
      rl.question(`${colors.cyan}请选择 [0-3]: ${colors.reset}`, (answer) => {
        switch(answer.trim()) {
          case '1':
            currentView = 'tools';
            verifyVersions = false; // 默认不验证
            displayToolSelectionMenu();
            break;
          case '2':
            rl.close();
            resolve({ action: 'upgrade-all' });
            break;
          case '3':
            console.log(`\n${colors.yellow}⚠ 正在验证所有工具状态，请稍候...${colors.reset}`);
            showAllToolsStatus();
            rl.question(`\n${colors.cyan}按回车键返回主菜单...${colors.reset}`, () => {
              displayMainMenu();
            });
            break;
          case '0':
            rl.close();
            resolve({ action: 'exit' });
            break;
          default:
            console.log(`${colors.red}无效选择，请重新输入${colors.reset}`);
            setTimeout(displayMainMenu, 500);
        }
      });
    }

    function displayToolSelectionMenu() {
      showToolSelectionMenu(selectedTools, verifyVersions);
      rl.question(`${colors.cyan}请操作: ${colors.reset}`, (answer) => {
        const input = answer.trim().toLowerCase();

        if (input === 'q' || input === 'quit') {
          currentView = 'main';
          displayMainMenu();
        } else if (input === 'a' || input === 'all') {
          Object.keys(CLI_TOOLS).forEach(key => selectedTools.add(key));
          displayToolSelectionMenu();
        } else if (input === 'n' || input === 'none') {
          selectedTools.clear();
          displayToolSelectionMenu();
        } else if (input === 'c' || input === 'change') {
          // 切换验证状态
          verifyVersions = !verifyVersions;
          if (verifyVersions) {
            console.log(`\n${colors.yellow}⚠ 正在验证工具状态，请稍候...${colors.reset}`);
          }
          displayToolSelectionMenu();
        } else if (input === '') {
          if (selectedTools.size === 0) {
            console.log(`${colors.yellow}请至少选择一个工具${colors.reset}`);
            setTimeout(displayToolSelectionMenu, 500);
          } else {
            rl.close();
            resolve({ action: 'upgrade-selected', tools: Array.from(selectedTools) });
          }
        } else {
          // 解析选择 - 使用显示顺序映射
          const numbers = input.split(' ').filter(n => /^\d+$/.test(n));

          // 获取显示顺序映射
          const displayOrderToKey = (typeof global !== 'undefined' && global.displayOrderToKey) ||
                                   (showToolSelectionMenu.displayOrderToKey || []);

          numbers.forEach(num => {
            const index = parseInt(num) - 1;
            if (index >= 0 && index < displayOrderToKey.length) {
              const key = displayOrderToKey[index];
              if (key && CLI_TOOLS[key]) {
                if (selectedTools.has(key)) {
                  selectedTools.delete(key);
                } else {
                  selectedTools.add(key);
                }
              }
            } else if (index >= 0 && index < Object.keys(CLI_TOOLS).length) {
              // 回退到旧的Object.keys方法（兼容性）
              const keys = Object.keys(CLI_TOOLS);
              const key = keys[index];
              if (selectedTools.has(key)) {
                selectedTools.delete(key);
              } else {
                selectedTools.add(key);
              }
            }
          });
          displayToolSelectionMenu();
        }
      });
    }

    function showAllToolsStatus() {
      console.log(`\n${colors.bright}═══════════════════════════════════════════${colors.reset}`);
      console.log(`${colors.bright}所有工具状态${colors.reset}`);
      console.log(`${colors.bright}═══════════════════════════════════════════${colors.reset}\n`);

      for (const [key, tool] of Object.entries(CLI_TOOLS)) {
        console.log(`${colors.cyan}${tool.displayName}${colors.reset} (${tool.package})`);

        // 只有在需要验证时才检查版本
        console.log(`  ${colors.dim}要查看详细状态，请在主菜单选择"查看所有工具状态"${colors.reset}`);
        console.log('');
      }
    }

    displayMainMenu();
  });
}

// 显示所有工具状态
function showAllToolsStatus() {
  console.log(`\n${colors.bright}═══════════════════════════════════════════${colors.reset}`);
  console.log(`${colors.bright}所有工具状态${colors.reset}`);
  console.log(`${colors.bright}═══════════════════════════════════════════${colors.reset}\n`);

  // 按类别分组工具
  const toolsByCategory = {};
  for (const [key, tool] of Object.entries(CLI_TOOLS)) {
    const category = tool.category || '其他';
    if (!toolsByCategory[category]) {
      toolsByCategory[category] = [];
    }
    toolsByCategory[category].push({ key, tool });
  }

  for (const [category, tools] of Object.entries(toolsByCategory)) {
    console.log(`${colors.cyan}━━━ ${category} ━━━${colors.reset}\n`);

    for (const { key, tool } of tools) {
      const currentVersion = getInstalledVersion(tool.package);
      const latestVersion = getLatestVersion(tool.package);
      const note = tool.note ? ` ${colors.dim}(${tool.note})${colors.reset}` : '';

      console.log(`${colors.cyan}${tool.displayName}${colors.reset} (${tool.package})${note}`);
      if (!currentVersion) {
        console.log(`  ${colors.red}状态: 未安装${colors.reset}`);
        console.log(`  ${colors.yellow}可安装版本: v${latestVersion || '未知'}${colors.reset}`);
      } else {
        console.log(`  ${colors.green}当前版本: v${currentVersion}${colors.reset}`);
        if (latestVersion && currentVersion !== latestVersion) {
          console.log(`  ${colors.yellow}最新版本: v${latestVersion}${colors.reset}`);
        } else {
          console.log(`  ${colors.green}已是最新版本${colors.reset}`);
        }
      }
      console.log('');
    }
  }
}

// 升级选定工具
function upgradeSelectedTools(toolKeys) {
  console.log(`\n${colors.bright}${colors.cyan}════════════════════════════════════════${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}开始升级选定的工具${colors.reset}`);
  console.log(`${colors.bright}${colors.cyan}════════════════════════════════════════${colors.reset}\n`);

  const results = {};
  for (const key of toolKeys) {
    if (CLI_TOOLS[key]) {
      results[key] = checkTool(key, CLI_TOOLS[key]);
    }
  }

  // 总结报告
  console.log(`\n${colors.bright}═══════════════════════════════════════${colors.reset}`);
  console.log(`${colors.bright}升级总结${colors.reset}`);
  console.log(`${colors.bright}═══════════════════════════════════════${colors.reset}\n`);

  let upgradeCount = 0;
  let installCount = 0;
  let latestCount = 0;

  for (const [key, result] of Object.entries(results)) {
    const tool = CLI_TOOLS[key];

    if (result.success) {
      if (result.isLatest) {
        latestCount++;
        console.log(`${colors.green}✓${colors.reset} ${tool.displayName}: 已是最新版本 (${result.currentVersion})`);
      } else if (result.upgraded) {
        upgradeCount++;
        console.log(`${colors.green}↑${colors.reset} ${tool.displayName}: 已升级到 ${result.newVersion}`);
      } else if (!result.currentVersion) {
        installCount++;
        console.log(`${colors.green}↓${colors.reset} ${tool.displayName}: 已安装 ${result.newVersion}`);
      }
    } else {
      console.log(`${colors.red}✗${colors.reset} ${tool.displayName}: 安装失败`);
    }
  }

  console.log(`\n${colors.bright}统计:${colors.reset}`);
  console.log(`  ${colors.green}新安装:${colors.reset} ${installCount}`);
  console.log(`  ${colors.green}已升级:${colors.reset} ${upgradeCount}`);
  console.log(`  ${colors.green}已是最新:${colors.reset} ${latestCount}`);
  console.log(`  ${colors.bright}选中的工具总数:${colors.reset} ${toolKeys.length}\n`);
}

// 主函数
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // 启动交互式模式
    const result = await interactiveMode();

    if (result.action === 'exit') {
      console.log(`${colors.green}已退出${colors.reset}\n`);
      process.exit(0);
    } else if (result.action === 'upgrade-all') {
      checkAllTools();
    } else if (result.action === 'upgrade-selected' && result.tools) {
      upgradeSelectedTools(result.tools);
    }
  } else if (args[0] === '--interactive' || args[0] === '-i') {
    // 强制使用交互模式
    const result = await interactiveMode();

    if (result.action === 'exit') {
      console.log(`${colors.green}已退出${colors.reset}\n`);
      process.exit(0);
    } else if (result.action === 'upgrade-all') {
      checkAllTools();
    } else if (result.action === 'upgrade-selected' && result.tools) {
      upgradeSelectedTools(result.tools);
    }
  } else if (args[0] === '--help' || args[0] === '-h') {
    console.log(`
${colors.bright}AI CLI 工具管理器 v1.2.1${colors.reset}

用法:
  ${colors.cyan}ai-cli-manager${colors.reset}                # 启动交互式菜单（推荐）
  ${colors.cyan}ai-cli-manager --interactive${colors.reset}  # 强制使用交互式菜单
  ${colors.cyan}ai-cli-manager --all${colors.reset}          # 升级所有工具（非交互）
  ${colors.cyan}ai-cli-manager --status${colors.reset}       # 查看所有工具状态
  ${colors.cyan}ai-cli-manager <tool-name>${colors.reset}    # 升级指定工具

工具名称:
  ${Object.keys(CLI_TOOLS).slice(0, 10).join(', ')}
  (共${Object.keys(CLI_TOOLS).length}个工具，更多请使用交互模式)

示例:
  ${colors.yellow}ai-cli-manager${colors.reset}                     # 交互式菜单
  ${colors.yellow}ai-cli-manager --all${colors.reset}              # 升级所有工具
  ${colors.yellow}ai-cli-manager gemini-cli${colors.reset}         # 只升级 gemini-cli
  ${colors.yellow}ai-cli-manager --status${colors.reset}           # 查看状态

交互模式快捷键:
  [空格] 选择/取消工具 | [A] 全选 | [N] 全不选 | [C] 切换验证模式 | [Q] 返回 | [回车] 确认

验证模式:
  快速模式（默认）- 快速显示，无需验证
  验证模式 - 显示安装状态和版本（较慢）
    `);
  } else if (args[0] === '--all') {
    // 升级所有工具（非交互）
    checkAllTools();
  } else if (args[0] === '--status') {
    // 查看所有工具状态
    showAllToolsStatus();
  } else {
    // 升级指定工具
    checkSingleTool(args[0]);
  }
}

// 运行
main().catch(error => {
  console.error(`\n${colors.red}错误: ${error.message}${colors.reset}`);
  process.exit(1);
});
