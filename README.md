# GitHub Action: Bump version

## Description

Action to bump version using [BumpVer](https://pypi.org/project/bumpver/).

Version component to bump or specific version to set are recognized by version bump flags

```
[bump version 2.5.0]

[bump ver major]

[bump ver minor]

[bump ver patch]

[bump ver]
```

The last one `[bump ver]` is used mostly in [CalVer](https://calver.org/) configuration.

Hint: helper action to parse flags [github.com/all4group/github-action-parse-flags](https://github.com/all4group/github-action-parse-flags)

## Requirements

Action requires `python` to be installed on `runner`.

Hint: [github.com/actions/setup-python](https://github.com/actions/setup-python)

## Inputs

```
component        - version component to bump (not required, not set by default)
                   i.e. 'major', 'minor', 'patch', 'empty'

version          - specific version to set (not required, not set by default)
                   i.e. '2.5.0'

primary          - primary string to parse component or version from (not required, not set by default)
                   i.e. 'Summer release [bump version major]'

secondary        - secondary string to parse component or version from (not required, not set by default)
                   i.e. 'Hotfix release [bump version patch]'

extra            - extra command line options (not required, not set by default)
                   i.e. '--tag beta --tag-num'
```

Inputs are evaluated in the following order

```
1. version

2. component

3. primary

4. secondary
```

In case `version` and `component` are not set then detected version bump flags are applied in the following order

```
1. [bump version X.Y.Z]

2. [bump ver major]

3. [bump ver minor]

4. [bump ver patch]
```

meaning, when there is more then one version bump flag then higher priority flag is used.

## Outputs

```
version          - version after bump
                   i.e. '2.5.0
```

## Usage

### Sample workflow definition `manual trigger`

```
name: Sample workflow

on:
  workflow_dispatch:
    inputs:
      component:
        description: "Version component to bump, i.e. 'major', 'minor', 'patch', 'empty'"
        required: false
        default: ""
      version:
        description: "Specific version to set, i.e. '2.5.0'"
        required: false
        default: ""
      extra:
        description: "Extra command line options"
        required: false
        default: ""

jobs:
  sample:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Initialize git
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
        shell: bash
      - name: Execute action bump version
        uses: all4group/github-action-bump-version@v2
        with:
          component: ${{ github.event.inputs.component }}
          version: ${{ github.event.inputs.version }}
          extra: ${{ github.event.inputs.extra }}
```

### Sample workflow definition `pull request` `closed` `merged`

```
name: Sample workflow

on:
  pull_request:
    branches:
      - main
    types: [closed]

jobs:
  sample:
    if: ${{ github.event.pull_request.merged }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Initialize git
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
        shell: bash
      - name: Execute action bump version
        uses: all4group/github-action-bump-version@v2
        with:
          primary: "'[${{ join(github.event.pull_request.labels.*.name, '];[') }}]'"
          secondary: "'${{ github.event.pull_request.title }}'"
```

### Sample workflow definition `push` with `extra`

```
name: Sample workflow

on:
  push:
    branches:
      - main

jobs:
  sample:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Initialize git
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
        shell: bash
      - name: Execute action bump version
        uses: all4group/github-action-bump-version@v2
        with:
          primary: "'${{ github.event.head_commit.message }}'"
          extra: "'--tag rc --tag-num'"
```
