import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathlint.citations import isbn_valid, url_ok  # noqa: E402
from mathlint.checks import check_text, citation_key  # noqa: E402
from mathlint.parser import scan  # noqa: E402

LONG = "这是一段足够长的论断，用来触发无标记检查，它包含完整的句子和明确的主张，因此应该被算作需要证据标记的段落。"


def codes(issues):
    return [i.code for i in issues]


class IdentifierTests(unittest.TestCase):
    def test_isbn13_valid(self):
        self.assertTrue(isbn_valid("978-3-16-148410-0"))

    def test_isbn13_invalid(self):
        self.assertFalse(isbn_valid("978-0-387-12345-6"))

    def test_isbn10_valid(self):
        self.assertTrue(isbn_valid("0-306-40615-2"))

    def test_isbn10_invalid(self):
        self.assertFalse(isbn_valid("0-306-40615-3"))

    def test_url_ok(self):
        self.assertTrue(url_ok("https://example.org/a/b"))
        self.assertFalse(url_ok("https://"))
        self.assertFalse(url_ok("example.org/a"))


class CitationCheckTests(unittest.TestCase):
    def test_bad_doi(self):
        result = check_text("f.md", "论断。〔S｜二手研究:Smith 2019, DOI:10.1234 bad〕")
        self.assertIn("CITATION_DOI", codes(result.issues))

    def test_good_doi(self):
        result = check_text("f.md", "论断。〔S｜二手研究:Smith 2019, DOI:10.1093/jhmas/jrab001, p. 3〕")
        self.assertNotIn("CITATION_DOI", codes(result.issues))

    def test_bad_ark(self):
        result = check_text("f.md", "论断。〔A｜原始文献:BnF 1696, ARK:12148/bpt6k205444w〕")
        self.assertIn("CITATION_ARK", codes(result.issues))

    def test_url_without_access_date(self):
        result = check_text("f.md", "论断。〔A｜原始文献:Newton 1687, p. 1；URL:https://www.newtonproject.ox.ac.uk/x〕")
        self.assertIn("CITATION_NO_ACCESS_DATE", codes(result.issues))

    def test_multiple_urls(self):
        text = "论断。〔A｜原始文献:Newton 1687；URL:https://a.org/x（访问 2026-11-13）；URL:https://b.org/y〕"
        result = check_text("f.md", text)
        self.assertIn("CITATION_MULTI_URL", codes(result.issues))

    def test_locator_without_digits(self):
        result = check_text("f.md", "论断。〔S｜二手研究:Grabiner, Origins of Cauchy Calculus〕")
        self.assertIn("LOCATOR_NO_LOCATION", codes(result.issues))


class SemanticCheckTests(unittest.TestCase):
    def test_missing_tag_on_long_paragraph(self):
        result = check_text("f.md", LONG)
        self.assertIn("MISSING_TAG", codes(result.issues))

    def test_tagged_paragraph_ok(self):
        result = check_text("f.md", LONG + "〔S｜二手研究:Grabiner 1981, p. 1〕")
        self.assertNotIn("MISSING_TAG", codes(result.issues))

    def test_short_sentence_not_counted(self):
        result = check_text("f.md", "这一步很关键。")
        self.assertNotIn("MISSING_TAG", codes(result.issues))

    def test_declared_sidebar_skipped(self):
        result = check_text("f.md", "> 旁栏（解释性文字，不承担推理）：" + LONG)
        self.assertNotIn("MISSING_TAG", codes(result.issues))

    def test_list_items_checked_separately(self):
        result = check_text("f.md", "- " + LONG + "\n- " + LONG + "〔S｜二手研究:Grabiner 1981, p. 1〕")
        missing = [i for i in result.issues if i.code == "MISSING_TAG"]
        self.assertEqual(len(missing), 1)

    def test_u_with_hollow_reason(self):
        result = check_text("f.md", "论断。〔U｜未核实:待查〕")
        self.assertIn("U_NO_REASON", codes(result.issues))

    def test_u_without_next_step(self):
        result = check_text("f.md", "论断。〔U｜未核实:仅见书目著录，未见原件，原因不详到无法判断〕")
        self.assertIn("U_NO_NEXT_STEP", codes(result.issues))

    def test_u_good(self):
        result = check_text("f.md", "论断。〔U｜未核实:仅见书目著录，未见原刊影像；待查 1684 年卷〕")
        self.assertNotIn("U_NO_REASON", codes(result.issues))
        self.assertNotIn("U_NO_NEXT_STEP", codes(result.issues))

    def test_wikipedia_as_a(self):
        result = check_text("f.md", "论断。〔A｜原始文献:维基百科条目〕")
        self.assertIn("GRADE_SOURCE_MISMATCH", codes(result.issues))

    def test_textbook_as_s(self):
        result = check_text("f.md", "论断。〔S｜二手研究:某教科书, p. 233〕")
        self.assertIn("GRADE_SOURCE_MISMATCH", codes(result.issues))

    def test_editorial_introduction_as_a(self):
        result = check_text("f.md", "论断。〔A｜原始文献:Opera omnia, 编者导言, p. vii〕")
        self.assertIn("GRADE_EDITORIAL", codes(result.issues))

    def test_author_preface_as_a_allowed(self):
        result = check_text("f.md", "论断。〔A｜原始文献:Euler E212, 作者自序, p. iii〕")
        self.assertNotIn("GRADE_EDITORIAL", codes(result.issues))

    def test_secondhand_as_a(self):
        result = check_text("f.md", "论断。〔A｜原始文献:转引自 Boyer 1949, p. 212；原文献 Cantor 1894, p. 89〕")
        self.assertIn("GRADE_SECONDHAND_A", codes(result.issues))

    def test_secondhand_unnamed(self):
        result = check_text("f.md", "论断。〔S｜二手研究:转引自某文献, p. 3〕")
        self.assertIn("SECONDHAND_UNNAMED", codes(result.issues))

    def test_translation_as_a(self):
        result = check_text("f.md", "论断。〔A｜原始文献:牛顿《原理》中译本, p. 41〕")
        self.assertIn("GRADE_TRANSLATION", codes(result.issues))

    def test_multi_grade(self):
        text = "一。〔S｜二手研究:Grabiner 1981, p. 47〕\n\n二。〔A｜原始文献:Grabiner 1981, p. 47〕"
        result = check_text("f.md", text)
        self.assertIn("MULTI_GRADE", codes(result.issues))

    def test_multi_grade_ignores_different_keys(self):
        text = "一。〔S｜二手研究:Grabiner 1981, p. 47〕\n\n二。〔A｜原始文献:Boyer 1949, p. 3〕"
        result = check_text("f.md", text)
        self.assertNotIn("MULTI_GRADE", codes(result.issues))

    def test_citation_key_normalisation(self):
        tags, _ = scan("a〔S｜二手研究:Grabiner 1981, pp. 45–52〕 b〔A｜原始文献:Grabiner 1981, p. 47〕")
        self.assertEqual(citation_key(tags[0]), citation_key(tags[1]))

    def test_citation_key_uses_doi(self):
        tags, _ = scan("〔S｜二手研究:X 2019, DOI:10.1093/jhmas/jrab001；转引自 Y 2020, p. 3〕")
        self.assertEqual(citation_key(tags[0]), "doi:10.1093/jhmas/jrab001")

    def test_inline_code_quoted_marker_not_an_error(self):
        text = "旧稿写作 `【原】`，新写法见 `〔A｜原始文献:Leibniz 1684, p. 467〕`。"
        result = check_text("f.md", text)
        self.assertEqual(codes(result.issues), [])
        self.assertEqual(result.tags, [])

    def test_inline_code_does_not_hide_real_tag(self):
        text = "句子里有 `code`。〔A｜原始文献:Leibniz 1684, p. 467〕"
        result = check_text("f.md", text)
        self.assertEqual(codes(result.issues), [])
        self.assertEqual(len(result.tags), 1)


if __name__ == "__main__":
    unittest.main()
