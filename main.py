from drafter import *
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# THEME: clean, minimal, modern look: light background, system sans-serif
# type, generous spacing, rounded controls, and a single indigo accent.
# ---------------------------------------------------------------------------
set_website_style("pico")

SANS = "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Menlo, Consolas, 'Courier New', monospace"

add_website_css("html, body", """
    background-color: #fafafa;
    color-scheme: light;
    margin: 0;
    padding: 0;
    width: 100%;
    min-height: 100vh;
""")
add_website_css("#drafter-body--", """
    background-color: #fafafa;
    color: #1f2937;
    font-family: """ + SANS + """;
    width: 100%;
    max-width: none;
    min-height: 100vh;
    box-sizing: border-box;
    padding: 48px 8vw 80px 8vw;
""")
add_website_css("#drafter-body-- h1", """
    color: #111827;
    font-family: """ + SANS + """;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
""")
add_website_css("#drafter-body-- h2", """
    color: #111827;
    font-family: """ + SANS + """;
    font-weight: 600;
    font-size: 1.15rem;
    letter-spacing: -0.01em;
    margin-top: 40px;
    margin-bottom: 8px;
""")
add_website_css("#drafter-body-- p, #drafter-body-- li", """
    color: #4b5563;
    font-family: """ + SANS + """;
    font-size: 1rem;
    line-height: 1.7;
""")
add_website_css("#drafter-body-- pre", """
    background: #f3f4f6;
    color: #111827;
    font-family: """ + MONO + """;
    font-size: 0.88rem;
    line-height: 1.6;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px 20px;
    overflow-x: auto;
    box-shadow: none;
""")
add_website_css("#drafter-body-- button", """
    background: #111827;
    color: #ffffff;
    border: none;
    border-radius: 999px;
    font-family: """ + SANS + """;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 9px 20px;
    width: auto;
    display: inline-block;
    margin: 4px 6px 4px 0;
    box-shadow: none;
    transition: background 0.15s ease, transform 0.15s ease;
""")
add_website_css("#drafter-body-- button:hover", """
    background: #4f46e5;
    transform: translateY(-1px);
""")
add_website_css("#drafter-body-- input, #drafter-body-- select", """
    background-color: #ffffff;
    color: #111827;
    font-family: """ + SANS + """;
    border: 1px solid #d1d5db;
    border-radius: 10px;
    box-shadow: none;
""")
add_website_css("#drafter-body-- input:focus, #drafter-body-- select:focus", """
    border-color: #4f46e5;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
""")
add_website_css("#drafter-body-- ul", """
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
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
    """Convert a non-negative decimal integer to a binary string.

    Args:
        number: The decimal integer to convert.

    Returns:
        The binary representation of the number as a string.
"""
    if number == 0:
        return "0"

    digits = ""
    while number > 0:
        remainder = number % 2
        digits = str(remainder) + digits
        number = number // 2
    return digits


def decimal_to_hexadecimal(number: int) -> str:
    """Convert a non-negative decimal integer to a hexadecimal string.

    Args:
        number: The decimal integer to convert.

    Returns:
        The hexadecimal representation of the number as a string.
"""
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
    """Return whether number contains only digits allowed by the selected base.

    Args:
        number: The number string to validate.
            base: The numeric base that determines which digits are allowed.

    Returns:
        True when every character is valid for the selected base; otherwise False.
"""
    if number == "":
        return False

    allowed_digits = "0123456789ABCDEF"

    for digit in number.upper():
        if digit not in allowed_digits[:base]:
            return False

    return True


def digit_value(digit: str) -> int:
    """Return the numeric value of one digit character (0-9, A-F).

    Args:
        digit: A single digit character to convert.

    Returns:
        The integer value represented by the digit character.
"""
    if digit.isdigit():
        return int(digit)
    return ord(digit.upper()) - ord("A") + 10


def convert_to_decimal(number: str, base: int) -> int:
    """Convert a valid binary, decimal, or hexadecimal string to decimal.

    Args:
        number: The number string being converted.
            base: The numeric base of the input number.

    Returns:
        The decimal integer represented by the input number.
"""
    number = number.upper()
    decimal_number = 0

    for digit in number:
        decimal_number = decimal_number * base + digit_value(digit)

    return decimal_number


def base_name(base: int) -> str:
    """Return the display name for a numeric base.

    Args:
        base: The numeric base whose display name is needed.

    Returns:
        The human-readable name of the base.
"""
    if base == 2:
        return "Binary"
    elif base == 16:
        return "Hexadecimal"
    return "Decimal"


def group_bits(binary: str) -> str:
    """Left-pad a binary string to a multiple of 4 and group it in nibbles.

    Args:
        binary: The binary string to group into four-bit sections.

    Returns:
        A string containing the grouped binary digits.
"""
    padding = (4 - len(binary) % 4) % 4
    padded = "0" * padding + binary
    groups = []

    for start in range(0, len(padded), 4):
        groups.append(padded[start:start + 4])

    return " ".join(groups)


def division_steps(number: int, base: int) -> str:
    """Return a repeated-division trace as aligned monospace text.

    Args:
        number: The non-negative decimal number being divided.
            base: The base used for repeated division.

    Returns:
        A multiline string showing each division, quotient, and remainder.
"""
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
    """Return the positional expansion of a number, e.g. 'F x 16^1 + ...'.

    Args:
        number: The number whose positional expansion is needed.
            base: The numeric base of the number.

    Returns:
        A string showing each digit multiplied by its base power.
"""
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
    """Build the terminal-style result block for the current conversion.

    Args:
        state: The current application state containing the conversion result.

    Returns:
        A formatted string summarizing the input and converted values.
"""
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
    """Format saved conversions as an aligned text table.

    Args:
        conversions: The list of Conversion records to display.

    Returns:
        A formatted string containing the saved conversion history.
"""
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
    """Return the navigation bar shown at the top of every page.

    Args:
        None.

    Returns:
        A list of buttons linking to the main website pages.
"""
    return [
        Button("Home", "home"),
        Button("Converter", "converter"),
        Button("Learn", "learn"),
        Button("Practice", "practice"),
        Button("History", "history"),
        "\n",
    ]


def conversion_page_content(state: State) -> list:
    """Build the converter page content.

    Args:
        state: The current application state used to display inputs and results.

    Returns:
        A list of Drafter page components for the converter page.
"""
    content = [Header("Number Systems Lab"), "Converter"]
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
    """Build the front page of the website.

    Args:
        state: The current application state passed to the home page.

    Returns:
        The Drafter home page.
"""
    return home(state)


@route
def home(state: State) -> Page:
    """Show the purpose of the website and its main navigation.

    Args:
        state: The current application state for the page.

    Returns:
        The Drafter home page containing the project introduction and navigation.
"""
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
    """Show the number conversion form.

    Args:
        state: The current application state containing conversion values.

    Returns:
        The Drafter converter page.
"""
    return Page(state, conversion_page_content(state))


# The form normally supplies number_text and input_base. Defaults keep the
# route safe when someone opens the route URL directly without form data.
@route
def convert_number(
    state: State, number_text: str = "", input_base: str = "Decimal"
) -> Page:
    """Validate the input, convert it, and save a successful conversion.

    Args:
        state: The current application state to update.
        number_text: The number entered by the user. Defaults to an empty string
            when the route is opened directly without submitted form data.
        input_base: The selected input number system. Defaults to Decimal.

    Returns:
        A Drafter page showing the conversion result or an input error.
"""
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
    """Show every successful conversion saved during this session.

    Args:
        state: The current application state containing conversion history.

    Returns:
        The Drafter history page.
"""
    content = [Header("Number Systems Lab"), "History"]
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
    """Remove all saved conversions from the current session.

    Args:
        state: The current application state whose history will be cleared.

    Returns:
        The Drafter history page after the history has been cleared.
"""
    state.conversion_history = []
    state.error_message = ""
    return history(state)


@route
def learn(state: State) -> Page:
    """Teach the repeated-division and positional methods.

    Args:
        state: The current application state for the learning page.

    Returns:
        The Drafter learning page with explanations and worked examples.
"""
    content = [Header("Number Systems Lab"), "Learn"]
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
    """Show the current practice problem.

    Args:
        state: The current application state containing the practice number.

    Returns:
        The Drafter practice page with the current question and answer field.
"""
    content = [Header("Number Systems Lab"), "Practice"]
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
    """Create a new practice problem and display it.

    Args:
        state: The current application state whose practice number will be changed.

    Returns:
        The Drafter practice page showing the new practice problem.
"""
    state.practice_number += 7
    return practice(state)


# The answer normally comes from the practice form. A default prevents a
# direct route visit from failing because practice_answer is missing.
@route
def check_answer(state: State, practice_answer: str = "") -> Page:
    """Check the user's practice answer and show feedback.

    Args:
        state: The current application state containing the practice problem.
        practice_answer: The binary answer submitted by the user. Defaults to an
            empty string when the route is opened directly.

    Returns:
        A Drafter page showing whether the submitted answer is correct.
"""
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
# Unit tests for helper functions and route behavior.
# Test state is kept local or inline so the module does not create global
# application-state variables.
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

assert_equal(convert_number(State("", 10, "", 0, [], 25), "FF", "Hexadecimal").state.decimal_result, 255)
assert_equal(
    convert_number(
        State("", 10, "", 0, [], 25), "FF", "Hexadecimal"
    ).state.conversion_history[-1].hexadecimal_value,
    "FF"
)

assert_equal(convert_number(State("", 10, "", 0, [], 25), "102", "Binary").state.error_message != "", True)

assert_has(check_answer(State("", 10, "", 0, [], 25), "0"), "Keep Practicing")

def test_new_practice_changes_question() -> None:
    """Test that the new-practice route changes the current question.

    Returns:
        None: The function raises an assertion error if the test fails.
    """
    new_question_state = State("", 10, "", 0, [], 25)
    new_practice(new_question_state)
    assert_equal(new_question_state.practice_number, 32)

test_new_practice_changes_question()

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
