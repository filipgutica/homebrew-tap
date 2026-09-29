class Devps < Formula
  include Language::Python::Shebang

  desc "See running dev servers, where they came from, and jump to or stop them"
  homepage "https://github.com/filipgutica/devps"
  url "https://github.com/filipgutica/devps/archive/refs/tags/v0.1.1.tar.gz"
  sha256 "10241bd3d6d3ad6a30e25b170f65181e0b609b247c72522093122c816661456b"
  license "MIT"

  depends_on "fzf"
  depends_on :macos
  depends_on "python@3.14"

  def install
    rewrite_shebang detected_python_shebang, "devps"
    bin.install "devps"
  end

  test do
    assert_equal version.to_s, shell_output("#{bin}/devps --version").strip
    assert_match "no dev server matches", shell_output("#{bin}/devps kill 1 2>&1")
  end
end
