class Annoterm < Formula
  desc "Local-first terminal Markdown review and editing"
  homepage "https://github.com/filipgutica/annoterm"
  url "https://github.com/filipgutica/annoterm/archive/refs/tags/v0.2.0.tar.gz"
  sha256 "328c9678dcd75fdf902e18d9c8274b6a36b9a13941b6f95ddd8cf81746e2ecef"
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
