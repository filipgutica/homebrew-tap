class Wtree < Formula
  desc "Git worktree listing, PR state, and cleanup from the terminal"
  homepage "https://github.com/filipgutica/wtree"
  url "https://github.com/filipgutica/wtree/archive/df56a44367322026be9b2d90560f906ad7f56c2e.tar.gz"
  version "0.1.0"
  sha256 "41601d3efa792d26e79771c075dd5e5d09cf4c9646e137987cc6e454fd4fd267"

  depends_on "node"
  uses_from_macos "git"

  def install
    system "npm", "ci", "--ignore-scripts"
    system "npm", "run", "build"
    system "npm", "install", *std_npm_args
    bin.install_symlink libexec.glob("bin/*")
  end

  test do
    assert_equal version.to_s, shell_output("#{bin}/wtree --version").strip
    system "git", "init", "--initial-branch=main"
    system "git", "-c", "user.name=Homebrew", "-c", "user.email=brew@example.com",
           "commit", "--allow-empty", "-m", "Initial commit"
    worktrees = JSON.parse(shell_output("#{bin}/wtree --no-pr --json"))
    assert_equal 1, worktrees.length
    assert_equal "main", worktrees.first.fetch("branch")
    assert worktrees.first.fetch("isMain")
  end
end
