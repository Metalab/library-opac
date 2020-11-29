## A note on locales

The locale "ebu_KE" is used, but it's not actually the language "Embu" spoken in Kenya. In fact it's the "uwu-ified" version of de_AT, but Babel does not support using custom locales such es de_UWU.

## Adding new messages

In the src folder, run the following command:

```
pybabel extract --mapping=babel-mapping.ini --output=locale/messages.pot --copyright-holder=Metalab --project=library-opac --version=1 ./
```
This will update the locale/messages.pot file with the messages found in the templates in templates/*.html.j2

After that run
``` bash
pybabel update --input-file=locale/messages.pot --output-dir=locale
```
to update the files for each locale. Proceed to translate the new messages, then run
``` bash
pybabel compile --directory=locale
```
to generate the .mo files used by the script later.

## Adding a new translation

In the src folder, run the following command:
``` bash
pybabel init --input-file=locale/messages.pot --output-dir=locale --locale=*localehere*
```
where localehere can be any locale shown by `#!bash pybabel --list-locales`

After you have translated the new locale (See the "Adding new messages" section), add the new locale to the config.yml file. Add an image for the new language that will be shown in the language switcher to static/img/locales. You can now generate the pages by [running the script](howtouse.md).
