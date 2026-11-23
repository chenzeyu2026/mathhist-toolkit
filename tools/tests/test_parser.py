import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathlint.parser import (  # noqa: E402
    legacy_marker_issues,
    mask_code_fences,
    mask_inline_code,
    mask_non_prose,
    scan,
)


def codes(issues):
    return [i.code for i in issues]


class TagScanningTests(unittest.TestCase):
    def test_valid_tag(self):
        tags, issues = scan("这是一句论断。〔A｜原始文献:Leibniz 1684, p. 467〕")
        self.assertEqual(issues, [])
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].grade, "A")
        self.assertEqual(tags[0].label, "原始文献")
        self.assertEqual(tags[0].locator, "Leibniz 1684, p. 467")

    def test_english_labels_accepted(self):
        tags, issues = scan("Claim。〔S｜secondary:Grabiner 1981, p. 47〕")
        self.assertEqual(issues, [])
        self.assertEqual(tags[0].label, "secondary")

    def test_missing_bar(self):
        _, issues = scan("〔A原始文献:Leibniz 1684〕")
        self.assertIn("TAG_NO_BAR", codes(issues))

    def test_unknown_grade(self):
        _, issues = scan("〔B｜二手研究:Grabiner 1981〕")
        self.assertIn("TAG_UNKNOWN_GRADE", codes(issues))

    def test_missing_colon(self):
        _, issues = scan("〔S｜二手研究 Grabiner 1981〕")
        self.assertIn("TAG_NO_COLON", codes(issues))

    def test_empty_locator(self):
        _, issues = scan("〔S｜二手研究:〕")
        self.assertIn("TAG_EMPTY_LOCATOR", codes(issues))

    def test_grade_label_mismatch(self):
        _, issues = scan("〔A｜二手研究:Boyer 1949〕")
        self.assertIn("TAG_GRADE_LABEL_MISMATCH", codes(issues))

    def test_fullwidth_colon_accepted(self):
        tags, issues = scan("〔A｜原始文献：Leibniz 1684〕")
        self.assertEqual(issues, [])
        self.assertEqual(tags[0].locator, "Leibniz 1684")

    def test_nested_tag(self):
        text = "〔S｜二手研究:Boyer 1949, p. 212（其注引〔A｜原始文献:Newton 1687〕）〕"
        tags, issues = scan(text)
        self.assertEqual(issues, [])
        self.assertEqual(len(tags), 1)
        self.assertEqual(len(tags[0].nested), 1)
        self.assertEqual(tags[0].nested[0].grade, "A")

    def test_nested_tag_errors_propagate(self):
        text = "〔S｜二手研究:Boyer 1949（见〔B｜二手研究:Cantor 1894〕）〕"
        _, issues = scan(text)
        self.assertIn("TAG_UNKNOWN_GRADE", codes(issues))

    def test_unclosed_tag_does_not_stop_scan(self):
        text = "〔A｜原始文献:Leibniz 1684\n下一行 〔S｜二手研究:Grabiner 1981, p. 1〕"
        tags, issues = scan(text)
        self.assertIn("TAG_UNCLOSED", codes(issues))
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].grade, "S")

    def test_halfwidth_brackets(self):
        _, issues = scan("[A｜原始文献:Leibniz 1684]")
        self.assertIn("TAG_HALFWIDTH", codes(issues))

    def test_stray_close(self):
        _, issues = scan("这是一个多余的括号〕")
        self.assertIn("TAG_STRAY_CLOSE", codes(issues))

    def test_adjacent_tags(self):
        tags, issues = scan("论断。〔S｜二手研究:Grabiner 1981〕〔A｜原始文献:Cauchy 1823, p. 12〕")
        self.assertEqual(issues, [])
        self.assertEqual([t.grade for t in tags], ["S", "A"])

    def test_legacy_marker(self):
        issues = legacy_marker_issues("阿基米德用过穷竭法。【原】")
        self.assertEqual(codes(issues), ["LEGACY_MARKER"])
        self.assertEqual(issues[0].severity, "error")

    def test_legacy_marker_composite(self):
        issues = legacy_marker_issues("这段话两个来源。【原/研】")
        self.assertEqual(codes(issues), ["LEGACY_MARKER"])

    def test_code_fence_masked(self):
        text = "正文。\n\n```text\n〔A｜假标记:示例〕\n```\n\n后文。"
        masked = mask_code_fences(text)
        self.assertNotIn("假标记", masked)
        self.assertEqual(len(masked.splitlines()), len(text.splitlines()))

    def test_line_and_column(self):
        tags, _ = scan("第一行\n第二行 〔A｜原始文献:Leibniz 1684〕")
        self.assertEqual(tags[0].line, 2)
        self.assertEqual(tags[0].col, 5)


class InlineCodeMaskingTests(unittest.TestCase):
    def test_single_backtick_hides_tag(self):
        masked = mask_inline_code("示例 `〔A｜原始文献:Leibniz 1684〕` 写法")
        self.assertNotIn("Leibniz", masked)
        self.assertIn("示例", masked)

    def test_double_backtick_span(self):
        masked = mask_inline_code("嵌套 ``a ` b`` 结束")
        self.assertNotIn("a ` b", masked)
        self.assertIn("结束", masked)

    def test_unterminated_backtick_kept(self):
        text = "没有闭合 `abc"
        self.assertEqual(mask_inline_code(text), text)

    def test_span_does_not_cross_lines(self):
        text = "上面 `abc\ndef` 下面"
        self.assertEqual(mask_inline_code(text), text)

    def test_offsets_and_lines_preserved(self):
        text = "第一行 `x`\n第二行 〔A｜原始文献:Leibniz 1684〕"
        masked = mask_inline_code(text)
        self.assertEqual(len(masked), len(text))
        self.assertEqual(len(masked.splitlines()), len(text.splitlines()))
        tags, issues = scan(masked)
        self.assertEqual(issues, [])
        self.assertEqual(tags[0].line, 2)

    def test_mask_non_prose_applies_both(self):
        text = "```\n〔B｜错等级:x〕\n```\n正文 `【原】` 与 〔A｜原始文献:Leibniz 1684〕"
        masked = mask_non_prose(text)
        self.assertNotIn("【原】", masked)
        self.assertNotIn("错等级", masked)
        tags, issues = scan(masked)
        self.assertEqual(issues, [])
        self.assertEqual(len(tags), 1)
        self.assertEqual(legacy_marker_issues(masked), [])


if __name__ == "__main__":
    unittest.main()
