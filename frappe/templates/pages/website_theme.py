# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import re
import frappe
from frappe.website.doctype.website_theme.website_theme import get_active_theme

no_sitemap = 1
base_template_path = "templates/pages/website_theme.css"

default_properties = {
	"background_color": "#ffffff",
	"top_bar_color": "#ffffff",
	"top_bar_text_color": "#000000",
	"footer_color": "#ffffff",
	"footer_text_color": "#000000",
	"font_size": "14px",
	"text_color": "#000000",
	"link_color": "#000000"
}

def get_context(context):
	"""returns web style"""
	website_theme = get_active_theme()
	if not website_theme:
		return {}

	prepare(website_theme)

	return { "theme": website_theme }

def prepare(theme):
	for d in default_properties:
		if not theme.get(d):
			theme.set(d, default_properties[d])

	webfonts = list(set(theme.get(key)
		for key in ("heading_webfont", 'text_webfont') if theme.get(key)))

	theme.webfont_import = "\n".join('@import url(@import url(http://fonts.googleapis.com/css?family={0}:400,300,400italic,700&subset=latin,latin-ext);)'\
		.format(font.replace(" ", "+")) for font in webfonts)

	# move @import from css field to the top of the css file
	if theme.css and "@import url" in theme.css:
		webfont_import = list(set(re.findall("@import url\([^\(\)]*\);", theme.css)))
		theme.webfont_import += "\n" + "\n".join(webfont_import)
		for wfimport in webfont_import:
			theme.css = theme.css.replace(wfimport, "")