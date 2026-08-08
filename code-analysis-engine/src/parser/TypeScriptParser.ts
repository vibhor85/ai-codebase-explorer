import * as fs from 'fs';
import * as ts from 'typescript';

/**
 * Read a file from disk and return a TypeScript SourceFile AST.
 */
export function parseFile(filePath: string): ts.SourceFile {
  const sourceCode = fs.readFileSync(filePath, 'utf-8');
  return ts.createSourceFile(
    filePath,
    sourceCode,
    ts.ScriptTarget.Latest,
    true,
  );
}

export default { parseFile };
