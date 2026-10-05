class Wtree < Formula
  desc "Git worktree listing, PR state, and cleanup from the terminal"
  homepage "https://github.com/filipgutica/wtree"
  url "https://github.com/filipgutica/wtree/archive/refs/tags/v0.7.0.tar.gz"
  sha256 "b1b8cfe6a567bfc51b9f8a498e08e59fc9a93ff3579d943290d87d8b36676f4d"

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
