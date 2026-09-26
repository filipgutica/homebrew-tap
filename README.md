# Filip's Homebrew tap

Install the terminal tools:

```sh
brew install filipgutica/tap/annoterm
brew install filipgutica/tap/wtree
```

- [annoterm](https://github.com/filipgutica/annoterm): terminal Markdown review and editing.
- [wtree](https://github.com/filipgutica/wtree): Git worktree listing, PR state, and cleanup. GitHub CLI (`gh`) is optional for PR state.

Both formulae build from source on macOS and Linux. Homebrew installs Rust as a build dependency for annoterm and Node as a runtime dependency for wtree. Initial formulae pin the existing `0.1.0` source commits; subsequent versions use stable GitHub release tags.

## Releases and formula updates

Each tool owns its version and releases. Conventional squash commits drive release PRs: `fix:` bumps patch, `feat:` bumps minor, and `!` or a `BREAKING CHANGE:` footer bumps major, including before `1.0.0`. Merge a tool's release PR to publish its version.

This tap checks stable releases every six hours. The **Update formulae** workflow can also be run manually from GitHub Actions. It downloads and hashes each newer release archive, then opens or updates one formula PR. It does not push to `main`.

Bot-created PRs may display **Approve workflows to run**. A maintainer must approve those runs, review the changes, and merge after the formula checks pass. Automation uses each repository's own `GITHUB_TOKEN`; no shared personal token is required.

To refresh installed tools:

```sh
brew update
brew upgrade annoterm wtree
```

## Local checks

```sh
brew audit --strict filipgutica/tap/annoterm filipgutica/tap/wtree
brew install --build-from-source filipgutica/tap/annoterm filipgutica/tap/wtree
brew test filipgutica/tap/annoterm filipgutica/tap/wtree
brew linkage --test filipgutica/tap/annoterm filipgutica/tap/wtree
```
