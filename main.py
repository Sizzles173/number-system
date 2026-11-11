from drafter import *
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# THEME: dark "engineering console" look with a faint blueprint grid,
# monospace type, cyan/green accents, and terminal-style output panels.
# ---------------------------------------------------------------------------
set_website_style("pico")

MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Courier New', monospace"

add_website_css("#drafter-body--", """
    background-color: #070b14;
    background-image:
        linear-gradient(rgba(34, 211, 238, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34, 211, 238, 0.045) 1px, transparent 1px);
    background-size: 32px 32px;
    color: #cbd5e1;
    font-family: """ + MONO + """;
    min-height: 100vh;
    padding: 24px 24px 56px 24px;
""")
add_website_css("#drafter-body-- h1", """
    color: #22d3ee;
    font-family: """ + MONO + """;
    font-weight: 800;
    font-size: 1.7rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 1px solid #155e75;
    padding-bottom: 10px;
    text-shadow: 0 0 14px rgba(34, 211, 238, 0.45);
""")
add_website_css("#drafter-body-- h2", """
    color: #4ade80;
    font-family: """ + MONO + """;
    font-weight: 700;
    font-size: 1.05rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 28px;
""")
add_website_css("#drafter-body-- h2::before", """
    content: "// ";
    color: #475569;
""")
add_website_css("#drafter-body-- p, #drafter-body-- li", """
    color: #cbd5e1;
    font-family: """ + MONO + """;
    font-size: 0.93rem;
    line-height: 1.7;
""")
add_website_css("#drafter-body-- pre", """
    background: #020617;
    color: #86efac;
    font-family: """ + MONO + """;
    font-size: 0.9rem;
    line-height: 1.55;
    border: 1px solid #164e63;
    border-left: 4px solid #22d3ee;
    border-radius: 6px;
    padding: 14px 18px;
    overflow-x: auto;
    box-shadow: 0 0 24px rgba(34, 211, 238, 0.07) inset;
""")
add_website_css("#drafter-body-- button", """
    background: rgba(34, 211, 238, 0.06);
    color: #22d3ee;
    border: 1px solid #22d3ee;
    border-radius: 4px;
    font-family: """ + MONO + """;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 8px 16px;
    margin: 4px 6px 4px 0;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.15);
    transition: all 0.15s ease;
""")
add_website_css("#drafter-body-- button:hover", """
    background: #22d3ee;
    color: #020617;
    box-shadow: 0 0 18px rgba(34, 211, 238, 0.6);
""")
add_website_css("#drafter-body-- input, #drafter-body-- select", """
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: """ + MONO + """;
    border: 1px solid #334155;
    border-radius: 4px;
""")
add_website_css("#drafter-body-- input:focus, #drafter-body-- select:focus", """
    border-color: #22d3ee;
    box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.2);
""")
add_website_css("#drafter-body-- ul", """
    background-color: rgba(15, 23, 42, 0.85);
    border: 1px solid #1e293b;
    border-left: 4px solid #4ade80;
    border-radius: 6px;
    padding: 14px 24px;
""")


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
@dataclass
class Conversion:
    """Store the important values from one successful conversion."""
    original_number: str
    decimal_system: int
    binary_value: str
    hexadecimal_value: str


@dataclass
class State:
    """Store information that needs to persist while the site is open."""
    current_input: str
    input_base: int
    error_message: str
    decimal_result: int
    conversion_history: list[Conversion]
    practice_number: int


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def decimal_to_binary(number: int) -> str:
    """Convert a non-negative decimal integer to a binary string."""
    if number == 0:
        return "0"

    digits = ""
    while number > 0:
        remainder = number % 2
        digits = str(remainder) + digits
        number = number // 2
    return digits


def decimal_to_hexadecimal(number: int) -> str:
    """Convert a non-negative decimal integer to a hexadecimal string."""
    if number == 0:
        return "0"

    digits = "0123456789ABCDEF"
    result = ""

    while number > 0:
        remainder = number % 16
        result = digits[remainder] + result
        number = number // 16

    return result


def is_valid_number(number: str, base: int) -> bool:
    """Return whether number contains only digits allowed by the selected base."""
    if number == "":
        return False

    allowed_digits = "0123456789ABCDEF"

    for digit in number.upper():
        if digit not in allowed_digits[:base]:
            return False

    return True


def digit_value(digit: str) -> int:
    """Return the numeric value of one digit character (0-9, A-F)."""
    if digit.isdigit():
        return int(digit)
    return ord(digit.upper()) - ord("A") + 10


def convert_to_decimal(number: str, base: int) -> int:
    """Convert a valid binary, decimal, or hexadecimal string to decimal."""
    number = number.upper()
    decimal_number = 0

    for digit in number:
        decimal_number = decimal_number * base + digit_value(digit)

    return decimal_number


def base_name(base: int) -> str:
    """Return the display name for a numeric base."""
    if base == 2:
        return "Binary"
    elif base == 16:
        return "Hexadecimal"
    return "Decimal"


def group_bits(binary: str) -> str:
    """Left-pad a binary string to a multiple of 4 and group it in nibbles."""
    padding = (4 - len(binary) % 4) % 4
    padded = "0" * padding + binary
    groups = []

    for start in range(0, len(padded), 4):
        groups.append(padded[start:start + 4])

    return " ".join(groups)


def division_steps(number: int, base: int) -> str:
    """Return a repeated-division trace as aligned monospace text."""
    digits = "0123456789ABCDEF"

    if number == 0:
        return "0 / " + str(base) + " = 0   remainder 0   ->  0"

    lines = []
    while number > 0:
        quotient = number // base
        remainder = number % base
        lines.append(
            str(number).rjust(8) + " / " + str(base).ljust(2)
            + " = " + str(quotient).rjust(8)
            + "   remainder " + str(remainder).rjust(2)
            + "   ->  " + digits[remainder]
        )
        number = quotient

    return "\n".join(lines)


def expansion(number: str, base: int) -> str:
    """Return the positional expansion of a number, e.g. 'F x 16^1 + ...'."""
    number = number.upper()
    terms = []
    length = len(number)

    for index in range(length):
        power = length - index - 1
        terms.append(
            str(digit_value(number[index])) + "*" + str(base) + "^" + str(power)
        )

    return " + ".join(terms)


def result_report(state: State) -> str:
    """Build the terminal-style result block for the current conversion."""
    binary_text = decimal_to_binary(state.decimal_result)
    hex_text = decimal_to_hexadecimal(state.decimal_result)

    lines = [
        "INPUT        : " + state.current_input + "  (base " + str(state.input_base) + ")",
        "DECIMAL      : " + str(state.decimal_result),
        "BINARY       : 0b" + group_bits(binary_text),
        "HEXADECIMAL  : 0x" + hex_text,
        "BIT LENGTH   : " + str(len(binary_text)) + " bit(s)",
        "BYTES NEEDED : " + str((len(binary_text) + 7) // 8),
    ]
    return "\n".join(lines)


def history_table(conversions: list[Conversion]) -> str:
    """Format saved conversions as an aligned text table."""
    lines = [
        "#".ljust(4) + "INPUT".ljust(14) + "DECIMAL".ljust(12)
        + "BINARY".ljust(24) + "HEX",
        "-" * 62,
    ]

    for index in range(len(conversions)):
        conversion = conversions[index]
        lines.append(
            str(index + 1).ljust(4)
            + conversion.original_number.ljust(14)
            + str(conversion.decimal_system).ljust(12)
            + group_bits(conversion.binary_value).ljust(24)
            + "0x" + conversion.hexadecimal_value
        )

    return "\n".join(lines)


def nav_buttons() -> list:
    """Return the navigation bar shown at the top of every page."""
    return [
        Button("Home", "home"),
        Button("Converter", "converter"),
        Button("Learn", "learn"),
        Button("Practice", "practice"),
        Button("History", "history"),
        "\n",
    ]


def conversion_page_content(state: State) -> list:
    """Build the converter page content."""
    content = [Header("Number Systems Lab"), "[ MODULE 01 : CONVERTER ]"]
    content.extend(nav_buttons())
    content.extend([
        Header("Input", 2),
        "Enter a value, select its radix, and run the conversion.",
        "\n",
        "VALUE",
        TextBox("number_text", state.current_input),
        "\n",
        "RADIX",
        SelectBox(
            "input_base",
            ["Decimal", "Binary", "Hexadecimal"],
            base_name(state.input_base)
        ),
        "\n",
        Button("Convert Number", "convert_number"),
        "\n",
    ])

    if state.error_message != "":
        content.extend([
            Header("Error", 2),
            PreformattedText("ERR  invalid input\n" + state.error_message),
        ])
    elif state.current_input != "":
        binary_text = decimal_to_binary(state.decimal_result)
        content.extend([
            Header("Output", 2),
            PreformattedText(result_report(state)),
            Header("Binary Division Trace (base 2)", 2),
            PreformattedText(division_steps(state.decimal_result, 2)),
            "Read the remainders from the bottom up: " + binary_text,
            Header("Hex Division Trace (base 16)", 2),
            PreformattedText(division_steps(state.decimal_result, 16)),
        ])

        if state.input_base != 10:
            content.extend([
                Header("Positional Expansion", 2),
                PreformattedText(
                    state.current_input + " (base " + str(state.input_base)
                    + ") = " + expansion(state.current_input, state.input_base)
                    + " = " + str(state.decimal_result)
                ),
            ])

        content.append("Result logged to session history.")

    return content


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------
@route
def index(state: State) -> Page:
    """Build the front page of the website."""
    return home(state)


@route
def home(state: State) -> Page:
    """Show the purpose of the website and its main navigation."""
    content = [Header("Number Systems Lab")]
    content.extend(nav_buttons())
    content.extend([
        "Convert between decimal, binary, and hexadecimal. See every division",
        "step, inspect bit patterns, and drill your skills.",
        Header("Supported Radices", 2),
        PreformattedText(
            "BASE  NAME          SYMBOLS              PREFIX\n"
            "----  ------------  -------------------  ------\n"
            "  2   binary        0 1                  0b\n"
            " 10   decimal       0-9                  -\n"
            " 16   hexadecimal   0-9 A-F              0x"
        ),
        "TIP: new to number systems? Start with the Learn page.",
    ])
    return Page(state, content)


@route
def converter(state: State) -> Page:
    """Show the number conversion form."""
    return Page(state, conversion_page_content(state))


@route
def convert_number(state: State, number_text: str, input_base: str) -> Page:
    """Validate the input, convert it, and save a successful conversion."""
    state.current_input = number_text.strip().upper()

    if input_base == "Binary":
        state.input_base = 2
    elif input_base == "Hexadecimal":
        state.input_base = 16
    else:
        state.input_base = 10

    if not is_valid_number(state.current_input, state.input_base):
        state.error_message = (
            "Enter a valid " + base_name(state.input_base).lower()
            + " number using only the allowed digits."
        )
        return Page(state, conversion_page_content(state))

    state.decimal_result = convert_to_decimal(
        state.current_input, state.input_base
    )
    state.error_message = ""

    binary_value = decimal_to_binary(state.decimal_result)
    hexadecimal_value = decimal_to_hexadecimal(state.decimal_result)

    state.conversion_history.append(
        Conversion(
            state.current_input,
            state.decimal_result,
            binary_value,
            hexadecimal_value
        )
    )

    return Page(state, conversion_page_content(state))


@route
def history(state: State) -> Page:
    """Show every successful conversion saved during this session."""
    content = [Header("Number Systems Lab"), "[ MODULE 03 : SESSION LOG ]"]
    content.extend(nav_buttons())
    content.extend([
        Button("Clear History", "clear_history"),
        "\n",
    ])

    if len(state.conversion_history) == 0:
        content.extend([
            Header("Log Empty", 2),
            PreformattedText("No conversions recorded yet.\nRun the converter to add entries."),
        ])
    else:
        content.extend([
            Header("Saved Conversions", 2),
            PreformattedText(history_table(state.conversion_history)),
            "Entries logged: " + str(len(state.conversion_history)),
        ])

    return Page(state, content)


@route
def clear_history(state: State) -> Page:
    """Remove all saved conversions from the current session."""
    state.conversion_history = []
    state.error_message = ""
    return history(state)


@route
def learn(state: State) -> Page:
    """Teach the repeated-division and positional methods."""
    content = [Header("Number Systems Lab"), "[ MODULE 02 : REFERENCE ]"]
    content.extend(nav_buttons())
    content.extend([
        "Understand the algorithms instead of only getting an answer.",
        Header("Place Values (Binary)", 2),
        PreformattedText(
            "BIT POSITION :   7    6    5    4    3    2    1    0\n"
            "WEIGHT (2^n) : 128   64   32   16    8    4    2    1"
        ),
        "Each bit is worth a power of two. Add the weights where the bit is 1.",
        Header("Decimal → Binary", 2),
        "1. Divide the decimal number by 2.",
        "2. Record the remainder (0 or 1).",
        "3. Divide the quotient by 2 again.",
        "4. Repeat until the quotient is 0.",
        "5. Read the remainders from bottom to top.",
        "Worked example: 25",
        PreformattedText(division_steps(25, 2) + "\n\nread upward: 11001"),
        Header("Decimal → Hexadecimal", 2),
        "1. Divide the decimal number by 16.",
        "2. Record the remainder.",
        "3. Use A-F for remainders 10-15.",
        "4. Repeat until the quotient is 0.",
        "5. Read the remainders from bottom to top.",
        "Worked example: 255",
        PreformattedText(division_steps(255, 16) + "\n\nread upward: FF"),
        Header("Any Base → Decimal", 2),
        "Multiply each digit by the base raised to its position, then add.",
        PreformattedText(
            "1011 (base 2)  = " + expansion("1011", 2) + " = " + str(convert_to_decimal("1011", 2)) + "\n"
            "2F   (base 16) = " + expansion("2F", 16) + " = " + str(convert_to_decimal("2F", 16))
        ),
        Header("Nibble Lookup Table", 2),
        PreformattedText(
            "HEX  BIN     HEX  BIN     HEX  BIN     HEX  BIN\n"
            " 0   0000     4   0100     8   1000     C   1100\n"
            " 1   0001     5   0101     9   1001     D   1101\n"
            " 2   0010     6   0110     A   1010     E   1110\n"
            " 3   0011     7   0111     B   1011     F   1111"
        ),
        "Four binary digits map to exactly one hexadecimal digit, so binary",
        "and hex convert to each other by grouping bits in fours.",
    ])
    return Page(state, content)


@route
def practice(state: State) -> Page:
    """Show the current practice problem."""
    content = [Header("Number Systems Lab"), "[ MODULE 04 : DRILL ]"]
    content.extend(nav_buttons())
    content.extend([
        Header("Challenge", 2),
        "Convert this decimal number to binary:",
        PreformattedText(">>> " + str(state.practice_number)),
        PreformattedText(
            "WEIGHT (2^n) : 128   64   32   16    8    4    2    1"
        ),
        "ANSWER",
        TextBox("practice_answer"),
        "\n",
        Button("Check Answer", "check_answer"),
    ])
    return Page(state, content)


@route
def new_practice(state: State) -> Page:
    """Create a new practice problem and display it."""
    state.practice_number += 7
    return practice(state)


@route
def check_answer(state: State, practice_answer: str) -> Page:
    """Check the user's practice answer and show feedback."""
    correct_answer = decimal_to_binary(state.practice_number)
    submitted = practice_answer.strip().upper()

    if submitted == correct_answer:
        return Page(state, [
            Header("Correct"),
            PreformattedText(
                "STATUS  : PASS\n"
                "INPUT   : " + str(state.practice_number) + "\n"
                "ANSWER  : " + submitted
            ),
            "Your answer " + submitted + " is correct!",
            "\n",
            Button("Try Another", "new_practice"),
            Button("Converter", "converter"),
            Button("Home", "home"),
        ])

    return Page(state, [
        Header("Keep Practicing"),
        PreformattedText(
            "STATUS    : FAIL\n"
            "YOUR ANS  : " + submitted + "\n"
            "EXPECTED  : " + correct_answer + "\n\n"
            + division_steps(state.practice_number, 2)
        ),
        "Compare your remainders with the trace above.",
        "\n",
        Button("Try Again", "practice"),
        Button("Review the Lesson", "learn"),
        Button("Home", "home"),
    ])


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------
# Unit tests for helper functions.
assert_equal(decimal_to_binary(0), "0")
assert_equal(decimal_to_binary(10), "1010")
assert_equal(decimal_to_hexadecimal(255), "FF")
assert_equal(convert_to_decimal("1010", 2), 10)
assert_equal(convert_to_decimal("FF", 16), 255)
assert_equal(is_valid_number("10101", 2), True)
assert_equal(is_valid_number("10201", 2), False)

# Additional edge-case and validation tests.
assert_equal(decimal_to_hexadecimal(0), "0")
assert_equal(decimal_to_hexadecimal(10), "A")
assert_equal(decimal_to_hexadecimal(15), "F")
assert_equal(decimal_to_hexadecimal(16), "10")
assert_equal(is_valid_number("FF", 16), True)
assert_equal(is_valid_number("G5", 16), False)
assert_equal(is_valid_number("102", 2), False)
assert_equal(is_valid_number("", 10), False)

# Tests for the new technical helpers.
assert_equal(digit_value("7"), 7)
assert_equal(digit_value("F"), 15)
assert_equal(group_bits("1"), "0001")
assert_equal(group_bits("11001"), "0001 1001")
assert_equal(group_bits("11111111"), "1111 1111")
assert_equal(expansion("1011", 2), "1*2^3 + 0*2^2 + 1*2^1 + 1*2^0")
assert_equal(base_name(2), "Binary")
assert_equal(base_name(10), "Decimal")
assert_equal(base_name(16), "Hexadecimal")
assert_equal(division_steps(0, 2), "0 / 2 = 0   remainder 0   ->  0")
assert_equal(len(division_steps(25, 2).split("\n")), 5)

hex_result = convert_number(
    State("", 10, "", 0, [], 25),
    "FF",
    "Hexadecimal"
)
assert_equal(hex_result.state.decimal_result, 255)
assert_equal(
    hex_result.state.conversion_history[-1].hexadecimal_value,
    "FF"
)

invalid_result = convert_number(
    State("", 10, "", 0, [], 25),
    "102",
    "Binary"
)
assert_equal(invalid_result.state.error_message != "", True)

wrong_result = check_answer(
    State("", 10, "", 0, [], 25),
    "0"
)
assert_has(wrong_result, "Keep Practicing")

new_question_state = State("", 10, "", 0, [], 25)
new_practice(new_question_state)
assert_equal(new_question_state.practice_number, 32)

# At least one test for each route.
assert_has(index(State("", 10, "", 0, [], 25)), Button("Converter", "converter"))
assert_has(home(State("", 10, "", 0, [], 25)), Button("Learn", "learn"))
assert_has(converter(State("", 10, "", 0, [], 25)), TextBox("number_text", ""))

assert_state(
    convert_number(State("", 10, "", 0, [], 25), "10", "Decimal"),
    State(
        "10",
        10,
        "",
        10,
        [Conversion("10", 10, "1010", "A")],
        25
    )
)

assert_has(history(State("", 10, "", 0, [], 25)), "No conversions")

assert_state(
    clear_history(
        State(
            "10",
            10,
            "",
            10,
            [Conversion("10", 10, "1010", "A")],
            25
        )
    ),
    State("10", 10, "", 10, [], 25)
)

assert_has(learn(State("", 10, "", 0, [], 25)), "Decimal → Binary")
assert_has(practice(State("", 10, "", 0, [], 25)), "Convert this decimal number to binary:")
assert_has(new_practice(State("", 10, "", 0, [], 25)), "Convert this decimal number to binary:")
assert_has(check_answer(State("", 10, "", 0, [], 25), "11001"), "correct")


# ---------------------------------------------------------------------------
# SITE SETTINGS
# ---------------------------------------------------------------------------
set_website_title("Number Systems Lab")
set_page_transition("fade", 0.25)
set_site_information(
    author="Soumil Ghosh",
    description=(
        "A learning tool that converts numbers between decimal, "
        "binary, and hexadecimal and teaches the conversion process."
    ),
    sources="Drafter documentation and course project planning document.",
    planning="Copy of CS1 Final Project 1_ Design.pdf",
    links=[]
)
set_website_framed(False)

start_server(
    State(
        current_input="",
        input_base=10,
        error_message="",
        decimal_result=0,
        conversion_history=[],
        practice_number=25
    )
)
