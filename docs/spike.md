# Spike 001 - Parsing TypeScript AST

## Objective

Validate that the TypeScript Compiler API can parse a TypeScript/TSX file and extract import statements.

---

## Question

> Can we discover import relationships using only the TypeScript AST?

---

## Sample Input

```tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import AuthService from "./services/AuthService";
import UserCard from "./components/UserCard";

export default function Login() {
  return <div>Hello</div>;
}
```

---

## Pipeline

```
Read File
    ↓
createSourceFile()
    ↓
SourceFile (AST)
    ↓
DFS (ts.forEachChild)
    ↓
ImportDeclaration
    ↓
moduleSpecifier
```

---

## Approach

1. Read the file using `fs.readFileSync()`.
2. Parse the source using `ts.createSourceFile()`.
3. Traverse the AST recursively using `ts.forEachChild()`.
4. Detect `ImportDeclaration` nodes.
5. Extract the imported module.

---

## Key Learnings

### Parsing

```ts
const sourceFile = ts.createSourceFile(...);
```

Converts source code into an AST (`SourceFile`).

---

### Traversal

```ts
ts.forEachChild(node, visit);
```

A recursive DFS is sufficient to visit every node.

---

### Detecting Imports

```ts
ts.isImportDeclaration(node)
```

The Compiler API provides type guards for AST nodes.

---

### Extracting the Module

Initial attempt:

```ts
node.moduleSpecifier.getText()
```

Output:

```
'react'
```

Observation:

`getText()` returns the original source code for the node.

---

Correct approach:

```ts
if (ts.isStringLiteral(node.moduleSpecifier)) {
    console.log(node.moduleSpecifier.text);
}
```

Output:

```
react
react-router-dom
./services/AuthService
./components/UserCard
```

Observation:

`moduleSpecifier` is declared as an `Expression`, but at runtime it is a `StringLiteral`.

A type guard is required before accessing `.text`.

---

## Result

Successfully extracted all import module paths from the AST.

---

## Architectural Notes

Current responsibility:

```
SourceFile
      ↓
ImportExtractor
      ↓
Import Relationships
```

`ImportExtractor` should **not**:

- Read files
- Know repository structure
- Resolve import paths

Its only responsibility is extracting import relationships from a parsed AST.

---

## Next Question

How do we resolve an import path such as:

```
./services/AuthService
```

to the corresponding file in the repository?