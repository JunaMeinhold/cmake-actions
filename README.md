# CMake Actions Workflows

This repository provides reusable GitHub Actions workflows for:

- **Building and uploading native artifacts with CMake**
- **Creating pull requests with trimmed artifacts**

> **Note:** These workflows are primarily designed to be used together with [HexaGen](https://github.com/HexaEngine/HexaGen), a C/COM to C# wrapper generator by JunaMeinhold.

## Workflows

### 1. Build and Upload Native Artifacts
Path: `cmake.yml`

Reusable workflow to build native libraries using CMake and upload artifacts.

**Example usage:**
```yaml
jobs:
  build:
    uses: JunaMeinhold/cmake-actions/cmake.yml@v1
    with:
      lib-name: MyLib
      repo: myorg/myrepo
      repo-tag: v1.0.0
      bin-name-osx: mylib.dylib
      bin-name-linux: mylib.so
      # ...other inputs as needed...
```

### 2. Create PR with Trimmed Artifacts
Path: `create-pr.yml`

Reusable workflow to download all artifacts, trim library names, and create a pull request.

**Example usage:**
```yaml
jobs:
  create-pr:
    uses: JunaMeinhold/cmake-actions/create-pr.yml@v1
    with:
      lib-name: MyLib
      repo-tag: v1.0.0
      output-dir: artifacts
      # ...other inputs as needed...
```

## Inputs
See each workflow file for a full list of supported inputs and their descriptions.

## License
This repository is licensed under the MIT License.
