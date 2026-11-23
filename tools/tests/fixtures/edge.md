# Fixture: 边界文档

这份文件用于测试边界行为：嵌套标记、英文来源类型、多个 URL、裸域名、无页码、表格内标记。

嵌套引用是合法写法：二手研究在自己的注释里转引了原始文献。〔S｜二手研究:Boyer 1949, p. 212（其注引〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II〕）〕

英文来源类型也接受。〔S｜secondary:Grabiner 1981, pp. 45–52〕

同一条里放两个 URL 会触发 warn。〔A｜原始文献:Newton, Principia, 1687；URL:https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00056（访问 2026-11-13）；URL:https://archive.org/details/principia〕

裸域名会触发 warn。〔A｜原始文献:L'Hôpital, Analyse des infiniment petits, 1696, p. 3；ARK:ark:/12148/bpt6k205444w（Gallica，访问 2026-11-13）；另见 www.gallica.bnf.fr〕

出处里没有任何数字，触发 warn。〔S｜二手研究:Grabiner, Origins of Cauchy's Rigorous Calculus〕

这条重复使用了同一个键但换了等级，触发 MULTI_GRADE。〔S｜二手研究:Grabiner 1981, p. 47〕〔A｜原始文献:Grabiner 1981, p. 47〕

> **误说**：微积分是牛顿和莱布尼茨凭空发明的。
> **纠正**：前有卡瓦列里、费马、沃利斯、巴罗，基本定理的几何形式在巴罗 1670 年已明确。〔A｜原始文献:Barrow, Lectiones geometricae, 1670, Lect. X〕〔S｜二手研究:Boyer 1949, ch. 4〕
