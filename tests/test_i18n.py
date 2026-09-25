import re
import sys
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Permite rodar a auditoria sem precisar inicializar o Flask inteiro.
if "flask" not in sys.modules:
    flask_stub = types.ModuleType("flask")
    flask_stub.session = {}
    sys.modules["flask"] = flask_stub

from services.i18n import TRANSLATIONS, translate

DYNAMIC_PREFIXES = (
    "game.achievement.", "game.activity.", "game.mission.", "game.rank.",
    "game.reward.", "game.skill.", "game.weekly_mission.",
)


def template_keys():
    keys = set()
    for path in (ROOT / "templates").rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        keys.update(re.findall(r"\{\{\s*t\(\s*['\"]([^'\"]+)['\"]", text))
    return {k for k in keys if not k.startswith(DYNAMIC_PREFIXES)}


class TranslationTests(unittest.TestCase):
    def test_all_static_template_keys_exist_in_every_language(self):
        keys = template_keys()
        for lang, values in TRANSLATIONS.items():
            missing = sorted(keys - values.keys())
            self.assertEqual(missing, [], f"{lang} missing: {missing}")

    def test_known_login_keys_are_translated(self):
        for lang in ("pt-BR", "en", "es"):
            for key in ("register.point1", "register.point2", "register.point3", "auth.home"):
                value = TRANSLATIONS[lang].get(key)
                self.assertTrue(value and value != key, f"{lang}: {key}")

    def test_unknown_translation_does_not_crash(self):
        self.assertEqual(translate("this.key.does.not.exist"), "this.key.does.not.exist")


if __name__ == "__main__":
    unittest.main()
