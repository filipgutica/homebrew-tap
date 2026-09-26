class Annoterm < Formula
  desc "Local-first terminal Markdown review and editing"
  homepage "https://github.com/filipgutica/annoterm"
  url "https://github.com/filipgutica/annoterm/archive/47d57bd0f9dae55a53519938fdf4ff30fb35975d.tar.gz"
  version "0.1.0"
  sha256 "3d73ba2491cb29f92a801d25637cd6a4d5630818e3c96f44b0030c015c0d7d7f"
  license "MIT"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/annoterm --version")
    (testpath/"document.md").write("# Homebrew installation\n")
    system bin/"annoterm", "export", "document.md", "--output", "feedback.md"
    assert_match "There are no open annotations.", (testpath/"feedback.md").read
  end
end
