import re
from pathlib import Path
import enchant

LANG = "en_US"


# we ignore shorter words
MIN_WORD_LENGTH = 3

# Latin words regexp
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# dialogue pattern
#   e "Hello there."
#   "Narrator line."
DIALOGUE_RE = re.compile(
    r'^\s*(?:\w+\s+)?\"(.+?)\"\s*$'
)

# any words we would like to exclude from spellchecking
IGNORE_WORDS = [
    "renpy",
]

USER_DICTIONARY = [
    "videogame", "webcomics", "Umm", "Umm", "Ummm"
]

CODE_PREFIXES = [
    "label ",
    "define ",
    "screen ",
    "transform ",
    "init ",
    "python:",
    "$",
    "if ",
    "elif ",
    "else:",
    "while ",
    "for ",
    "return",
    "menu:",
    "jump ",
    "call ",
    "image ",
    "style ",
    "default ",
    "layeredimage ",
    "thumb",
    "background",
    "foreground",
    "add",
    "textbutton",
    "font",
    "#",
]


def is_probably_code(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    for prefix in CODE_PREFIXES:
        if stripped.startswith(prefix):
            return True
    return False


def extract_dialogue(line: str) -> str | None:
    if is_probably_code(line):
        return None

    m = DIALOGUE_RE.match(line)
    if not m:
        return None

    text = m.group(1)

    # remove inserts, like [player] or {color}
    text = re.sub(r"\[.*?]", " ", text)
    text = re.sub(r"\{.*?}", " ", text)

    return text.strip()


def find_typos(text: str, dictionary: enchant.Dict) -> set[str]:
    typos: set[str] = set()

    for match in WORD_RE.finditer(text):
        word = match.group(0)

        w_lower = word.lower()

        if len(w_lower) < MIN_WORD_LENGTH:
            continue
        if w_lower in IGNORE_WORDS:
            continue

        if word.isupper():
            continue

        if not dictionary.check(word):
            typos.add(word)

    return typos


def iter_rpy_files(root: Path):
    for path in root.rglob("*.rpy"):
        relpath = path.relative_to(root)
        if relpath.parts[0] == "tl":
            continue
        yield path


def main() -> int:
    base_dir = Path(__file__).resolve().parent

    search_root = base_dir / "game"
    if not search_root.exists():
        print(f"game folder doesnt exist at {search_root}")
        return 1

    dictionary = enchant.Dict(LANG)

    for word in USER_DICTIONARY:
        dictionary.add(word)

    any_typos = False

    for rpy_path in iter_rpy_files(search_root):
        rel_path = rpy_path.relative_to(base_dir).as_posix()

        with rpy_path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                text = extract_dialogue(line)
                if not text:
                    continue

                typos = find_typos(text, dictionary)
                if not typos:
                    continue

                any_typos = True
                typos_list = ", ".join(sorted(typos))
                message = (
                    f"Possibly misspelled words: {typos_list} | Text: {text}"
                )

                print(f"::warning file={rel_path},line={lineno}::{message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
