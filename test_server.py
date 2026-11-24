import io
import unittest
from unittest.mock import patch

from server import translate_text


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class TranslationTests(unittest.TestCase):
    def test_requires_supported_different_languages(self):
        with self.assertRaisesRegex(ValueError, "Only English"):
            translate_text("Hello", "fr", "ko")
        with self.assertRaisesRegex(ValueError, "must be different"):
            translate_text("Hello", "en", "en")

    def test_rejects_empty_and_overlong_text(self):
        with self.assertRaisesRegex(ValueError, "Enter text"):
            translate_text("  ", "en", "ko")
        with self.assertRaisesRegex(ValueError, "500 characters"):
            translate_text("a" * 501, "en", "ko")

    @patch("server.urllib.request.urlopen")
    def test_returns_translated_text(self, urlopen):
        urlopen.return_value = FakeResponse(
            '{"responseData":{"translatedText":"안녕하세요"}}'.encode("utf-8")
        )

        result = translate_text("Hello", "en", "ko")

        self.assertEqual(result, "안녕하세요")
        request = urlopen.call_args.args[0]
        self.assertIn("langpair=en%7Cko", request.full_url)


if __name__ == "__main__":
    unittest.main()
