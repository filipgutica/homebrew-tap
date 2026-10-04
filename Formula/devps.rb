class Devps < Formula
  desc "See running dev servers, where they came from, and jump to or stop them"
  homepage "https://github.com/filipgutica/devps"
  url "https://github.com/filipgutica/devps/archive/refs/tags/v0.3.0.tar.gz"
  sha256 "eeb64f50c129f8c7ad4cb5c8f20f7faf94a6ed5b9ae2a7aa7b150b0150080993"
  license "MIT"

  depends_on "fzf"
  depends_on :macos
  depends_on "node"

  def install
    system "npm", "ci", "--ignore-scripts"
    system "npm", "run", "build"
    system "npm", "install", *std_npm_args
    bin.install_symlink libexec.glob("bin/*")
  end

  test do
    assert_equal version.to_s, shell_output("#{bin}/devps --version").strip
    assert_match "no dev server matches", shell_output("#{bin}/devps kill 1 2>&1")
  end
end
