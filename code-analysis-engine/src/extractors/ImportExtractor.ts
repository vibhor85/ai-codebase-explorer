import path from 'node:path';
import * as ts from 'typescript';
import type { ImportResolver } from '../resolver/ImportResolver.js';

export class ImportExtractor {
  constructor(
    private repositoryRoot: string,
    private importResolver: ImportResolver,
  ) {
    this.repositoryRoot = repositoryRoot;
    this.importResolver = importResolver;
  }

  extract(source: ts.SourceFile) {
    const relationships: { source: string; target: string }[] = [];
    const visit = (node: ts.Node) => {
      if (ts.isImportDeclaration(node)) {
        if (ts.isStringLiteral(node.moduleSpecifier)) {
          const target = this.importResolver.resolve(
            node.moduleSpecifier.text,
            source,
          );
          relationships.push({
            source: path.relative(this.repositoryRoot, source.fileName),
            target: target ?? node.moduleSpecifier.text,
          });
        }
      }
      // Ensure `this` is preserved when recursing by using an arrow wrapper
      ts.forEachChild(node, visit);
    };
    visit(source);
    return relationships;
  }
}
