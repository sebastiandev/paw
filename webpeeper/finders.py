import re
import unicodedata


class Finder(object):

    name = 'Finder'
    url = None
    keywords = []

    element_expr = None
    title_expr = None
    content_expr = None
    date_expr = None
    link_expr = None

    def _remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def _title(self, element):
        title = element.xpath(self.title_expr)
        return ''.join(title) if type(title) is list else title

    def _date(self, element):
        post_date = element.xpath(self.date_expr)
        post_date = ''.join(post_date) if type(post_date) is list else post_date
        re_match = re.search(r"\d{2}/\d{2}/\d{4}", post_date)
        return  re_match.group() if re_match else ''

    def _content(self, element):
        content = element.xpath(self.content_expr)
        return ''.join(content) if type(content) is list else content

    def _link(self, element):
        link = element.xpath(self.link_expr)
        return ''.join(link) if type(link) is list else link

    def _has_interesting_data(self, element, title, content, link, element_date):
        return any(k in self._remove_accents(content.lower()) for k in self.keywords) or \
               any(k in self._remove_accents(title.lower()) for k in self.keywords)

    def find(self, html_root):
        findings = []

        for element in html_root.xpath(self.element_expr):
            title = self._title(element)
            content = self._content(element)
            link = self._link(element)
            element_date = self._date(element)

            if self._has_interesting_data(element, title, content, link, element_date):
                findings.append((title, content, element_date, link))

        return findings


class PromocionesAereasFinder(Finder):

    name = "Promociones Aereas"
    url = "https://promociones-aereas.com.ar"
    keywords = ['costa rica', 'panama', 'mexico', 'caribe']

    element_expr = '//article'
    title_expr = './/header/h2/a/text()'
    content_expr = './/div/p/text()'
    date_expr = './/header/h6/text()'
    link_expr = './/header/h2/a/@href'
