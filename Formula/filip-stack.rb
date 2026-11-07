class FilipStack < Formula
  desc "Apply shared agent guidance and setup for Claude and Codex"
  homepage "https://github.com/filipgutica/filip-stack"
  url "https://github.com/filipgutica/filip-stack/archive/refs/tags/cli-v1.1.0.tar.gz"
  sha256 "e2c6bf4789c94520a544839bf07183f40dccf0e4b61f7f0d7ae2e37a8a8c585d"
  license "MIT"

  depends_on "node"
  uses_from_macos "git"

  def install
    libexec.install "cli"
    bin.install_symlink libexec/"cli/filip-stack.mjs" => "filip-stack"
  end

  def caveats
    <<~EOS
      Host config comes from a separate checkout on main:
        git clone https://github.com/filipgutica/filip-stack.git ~/code/filip-stack
        filip-stack apply
      For another checkout path, use filip-stack --repo <dir> <command>.
    EOS
  end

  test do
    assert_equal version.to_s, shell_output("#{bin}/filip-stack --version").strip
    assert_match "Usage: filip-stack", shell_output("#{bin}/filip-stack --help")
    assert_match "no source checkout", shell_output("#{bin}/filip-stack --repo #{testpath}/missing status 2>&1", 1)
  end
end
