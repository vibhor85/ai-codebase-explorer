import { ImportExtractor } from '../extractors/ImportExtractor.js';
import { parseFile } from '../parser/TypeScriptParser.js';
import { ImportResolver } from '../resolver/ImportResolver.js';

export interface AnalysisRequest {
  repositoryRoot: string;
  files: string[];
}

export interface Relationship {
  source: string;
  target: string | null;
}

export class CodeAnalysisEngine {
  analyze(request: AnalysisRequest): Relationship[] {
    const importResolver = new ImportResolver(request.repositoryRoot);
    const importExtractor = new ImportExtractor(
      request.repositoryRoot,
      importResolver,
    );

    return request.files.flatMap((filePath) => {
      const sourceFile = parseFile(filePath);
      const extractedRelationships = importExtractor.extract(sourceFile);

      return extractedRelationships.map((relationship) => ({
        source: relationship.source,
        target: relationship.target ?? null,
      }));
    });
  }
}
