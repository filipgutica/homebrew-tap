class Devps < Formula
  desc "See running dev servers, where they came from, and jump to or stop them"
  homepage "https://github.com/filipgutica/devps"
  url "https://github.com/filipgutica/devps/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "6b6385255153cf29456c69636857000d511d945da44cc4337d70b8c328ed40c5"
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
