import * as path from 'path';
import { parseFile } from './parser/TypeScriptParser.js';
import { ImportExtractor } from './extractors/ImportExtractor.js';
import { ImportResolver } from './resolver/ImportResolver.js';

const repoDir =
  '/Users/vibhorkumar/AI/AI-Codebase-Explorer/code-analysis-engine/samples';

const filePath = path.join(process.cwd(), 'samples', 'Login.tsx');

const sourceFile = parseFile(filePath);

const importResolver = new ImportResolver(repoDir);
const importExtractor = new ImportExtractor(repoDir, importResolver);
const relationships = importExtractor.extract(sourceFile);
console.log('relationships:', relationships);
