import path from 'path';
import * as ts from 'typescript';

export class ImportResolver {
  constructor(private repositoryRoot: string) {}

  resolve(importPath: string, sourceFile: ts.SourceFile) {
    const compilerOptions: ts.CompilerOptions = {
      moduleResolution: ts.ModuleResolutionKind.NodeNext,
    };
    const result = ts.resolveModuleName(
      importPath,
      sourceFile.fileName,
      compilerOptions,
      ts.sys,
    );

    if (!result.resolvedModule?.resolvedFileName) return null;

    return path.relative(
      this.repositoryRoot,
      result.resolvedModule?.resolvedFileName,
    );
  }
}
