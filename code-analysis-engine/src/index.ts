import { CodeAnalysisEngine } from './engine/CodeAnalysisEngine.js';
import type { AnalysisRequest } from './engine/CodeAnalysisEngine.js';

let input = '';

process.stdin.on('data', (chunk) => {
  input += chunk;
});

process.stdin.on('end', () => {
  let request: AnalysisRequest;

  try {
    request = JSON.parse(input) as AnalysisRequest;
  } catch (error) {
    console.error(
      'Failed to parse JSON input:',
      error instanceof Error ? error.message : error,
    );
    process.exit(1);
    return;
  }

  const engine = new CodeAnalysisEngine();

  let relationships;

  try {
    relationships = engine.analyze(request);
  } catch (error) {
    console.error(
      'Analysis failed:',
      error instanceof Error ? error.message : error,
    );
    process.exit(1);
    return;
  }

  const output = {
    relationships,
  };

  process.stdout.write(JSON.stringify(output));
});
