#!/bin/bash 

PRODUCT="biapy.fields.shorttitle"

mkdir -p locales/en/LC_MESSAGES/

i18ndude rebuild-pot --pot locales/$PRODUCT.pot --create $PRODUCT ./
i18ndude sync --pot locales/$PRODUCT.pot locales/*/LC_MESSAGES/$PRODUCT.po 

