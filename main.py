from drafter import *
from dataclasses import dataclass


# Use a colorful built-in theme and a few simple custom styles to make the
# learning pages easier to read and more visually engaging.
set_website_style("pico")
add_website_css("#drafter-body--", """
    background: linear-gradient(135deg, #eef6ff 0%, #f8f1ff 50%, #fff7ed 100%);
    min-height: 100vh;
    padding-bottom: 40px;
""")
add_website_css("#drafter-body-- h1", """
    color: #4f46e5;
    font-weight: 800;
    letter-spacing: 1px;
""")
add_website_css("#drafter-body-- h2", """
    color: #0f766e;
    font-weight: 750;
""")
add_website_css("#drafter-body-- button", """
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.20);
    margin: 4px;
""")
add_website_css("#drafter-body-- button:hover", """
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    transform: translateY(-1px);
""")
add_website_css("#drafter-body-- input, #drafter-body-- select", """
    border: 2px solid #c4b5fd;
    border-radius: 9px;
    background-color: white;
""")
add_website_css("#drafter-body-- input:focus, #drafter-body-- select:focus", """
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
""")
add_website_css("#drafter-body-- ul", """
    background-color: rgba(255, 255, 255, 0.82);
    border-left: 5px solid #8b5cf6;
    border-radius: 10px;
    padding: 14px 24px;
""")
add_website_css("#drafter-body-- p", """
    line-height: 1.6;
""")


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


def convert_to_decimal(number: str, base: int) -> int:
    """Convert a valid binary, decimal, or hexadecimal string to decimal."""
    number = number.upper()
    decimal_number = 0

    for digit in number:
        if digit.isdigit():
            digit_value = int(digit)
        else:
            digit_value = ord(digit) - ord("A") + 10

        decimal_number = decimal_number * base + digit_value

    return decimal_number


def base_name(base: int) -> str:
    """Return the display name for a numeric base."""
    if base == 2:
        return "Binary"
    elif base == 16:
        return "Hexadecimal"
    return "Decimal"


def conversion_page_content(state: State) -> list:
    """Build the converter page content."""
    content = [
        Header("🔢 NUMBER SYSTEMS LAB"),
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "Convert numbers and learn how decimal, binary, and hexadecimal work.",
        "\n",
        Button("🏠 Home", "home"),
        Button("📖 Learn", "learn"),
        Button("📜 History", "history"),
        Button("🎯 Practice", "practice"),
        "\n",
        Header("CONVERTER"),
        "Enter a number below, choose its original number system, and convert it.",
        "\n",
        "NUMBER",
        TextBox("number_text", state.current_input),
        "\n",
        "ORIGINAL NUMBER SYSTEM",
        SelectBox(
            "input_base",
            ["Decimal", "Binary", "Hexadecimal"],
            base_name(state.input_base)
        ),
        "\n",
        Button("✨ Convert Number", "convert_number"),
        "\n",
    ]

    if state.error_message != "":
        content.extend([
            Header("⚠️ CHECK YOUR INPUT"),
            state.error_message,
            "\n",
        ])
    elif state.current_input != "":
        binary_text = decimal_to_binary(state.decimal_result)
        hex_text = decimal_to_hexadecimal(state.decimal_result)
        content.extend([
            Header("✅ CONVERSION RESULT"),
            "Decimal",
            str(state.decimal_result),
            "\n",
            "Binary",
            binary_text,
            "\n",
            "Hexadecimal",
            hex_text,
            "\n",
            "Your number has been saved to your conversion history.",
        ])

    return content


@route
def index(state: State) -> Page:
    """Build the front page of the website."""
    return home(state)


@route
def home(state: State) -> Page:
    """Show the purpose of the website and its main navigation."""
    return Page(state, [
        Header("🔢 NUMBER SYSTEMS LAB"),
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "Learn • Convert • Practice",
        "\n",
        "A simple interactive lab for learning decimal, binary, and hexadecimal.",
        "Convert numbers, see the results instantly, and practice your skills.",
        "\n",
        Header("WHAT DO YOU WANT TO DO?"),
        "Convert a number",
        Button("✨ Open Converter", "converter"),
        "\n",
        "Learn how conversions work",
        Button("📖 Learn Conversions", "learn"),
        "\n",
        "Review your previous answers",
        Button("📜 View History", "history"),
        "\n",
        "Test what you know",
        Button("🎯 Start Practice", "practice"),
        "\n",
        "TIP: Start with Learn if you are new to number systems.",
    ])


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
    content = [
        Header("📜 CONVERSION HISTORY"),
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "Your successful conversions from this session.",
        "\n",
        Button("🏠 Home", "home"),
        Button("✨ Converter", "converter"),
        Button("🗑 Clear History", "clear_history"),
        "\n\n",
    ]

    if len(state.conversion_history) == 0:
        content.extend([
            Header("YOUR HISTORY IS EMPTY"),
            "Complete a conversion to see it appear here.",
        ])
    else:
        content.append(Header("SAVED CONVERSIONS"))
        history_lines = []

        for conversion in state.conversion_history:
            history_lines.append(
                conversion.original_number
                + "  →  Decimal: " + str(conversion.decimal_system)
                + "  |  Binary: " + conversion.binary_value
                + "  |  Hex: " + conversion.hexadecimal_value
            )

        content.append(BulletedList(history_lines))

    return Page(state, content)


@route
def clear_history(state: State) -> Page:
    """Remove all saved conversions from the current session."""
    state.conversion_history = []
    state.error_message = ""
    return history(state)


@route
def learn(state: State) -> Page:
    """Teach the basic repeated-division method for each number system."""
    return Page(state, [
        Header("📖 LEARN NUMBER SYSTEMS"),
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "Learn the ideas behind the conversions instead of only getting an answer.",
        "\n",
        Button("🏠 Home", "home"),
        Button("✨ Converter", "converter"),
        Button("🎯 Practice", "practice"),
        "\n",
        Header("DECIMAL → BINARY"),
        "Binary uses only 0 and 1.",
        "1. Divide the decimal number by 2.",
        "2. Record the remainder.",
        "3. Divide the quotient by 2 again.",
        "4. Repeat until the quotient is 0.",
        "5. Read the remainders from bottom to top.",
        "\n",
        Header("DECIMAL → HEXADECIMAL"),
        "Hexadecimal uses 0-9 and A-F.",
        "1. Divide the decimal number by 16.",
        "2. Record the remainder.",
        "3. Use A-F for remainders 10-15.",
        "4. Repeat until the quotient is 0.",
        "5. Read the remainders from bottom to top.",
        "\n",
        Header("💡 QUICK FACT"),
        "Four binary digits represent one hexadecimal digit.",
        "That is why binary and hexadecimal can be converted between so easily.",
    ])


@route
def practice(state: State) -> Page:
    """Show the current practice problem."""
    return Page(state, [
        Header("🎯 PRACTICE MODE"),
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        "Test yourself without looking at the converter first.",
        "\n",
        Button("🏠 Home", "home"),
        Button("📖 Learn", "learn"),
        Button("✨ Converter", "converter"),
        "\n",
        Header("YOUR CHALLENGE"),
        "Convert this decimal number to binary:",
        "\n",
        "⭐ " + str(state.practice_number) + " ⭐",
        "\n",
        "YOUR ANSWER",
        TextBox("practice_answer"),
        "\n",
        Button("✓ Check Answer", "check_answer"),
    ])


@route
def new_practice(state: State) -> Page:
    """Create a new practice problem and display it."""
    state.practice_number += 7
    return practice(state)


@route
def check_answer(state: State, practice_answer: str) -> Page:
    """Check the user's practice answer and update the feedback."""
    correct_answer = decimal_to_binary(state.practice_number)

    state.current_input = practice_answer.strip().upper()

    if state.current_input == correct_answer:
        state.error_message = ""
        return Page(state, [
            Header("🎉 CORRECT!"),
            "Your answer " + state.current_input + " is correct!",
            "You converted " + str(state.practice_number) + " successfully.",
            "\n",
            Button("➡ Try Another", "new_practice"),
            Button("✨ Converter", "converter"),
            Button("🏠 Home", "home"),
        ])

    state.error_message = "The correct answer is " + correct_answer + "."
    return Page(state, [
        Header("💪 KEEP PRACTICING"),
        "Your answer was " + state.current_input + ".",
        "\n",
        state.error_message,
        "\n\n",
        Button("↻ Try Again", "practice"),
        Button("📖 Review the Lesson", "learn"),
        Button("🏠 Home", "home"),
    ])


# Unit tests for helper functions.
assert_equal(decimal_to_binary(0), "0")
assert_equal(decimal_to_binary(10), "1010")
assert_equal(decimal_to_hexadecimal(255), "FF")
assert_equal(convert_to_decimal("1010", 2), 10)
assert_equal(convert_to_decimal("FF", 16), 255)
assert_equal(is_valid_number("10101", 2), True)
assert_equal(is_valid_number("10201", 2), False)

# Additional edge-case and validation tests.
assert_equal(decimal_to_binary(0), "0")
assert_equal(decimal_to_hexadecimal(0), "0")
assert_equal(decimal_to_hexadecimal(10), "A")
assert_equal(decimal_to_hexadecimal(15), "F")
assert_equal(decimal_to_hexadecimal(16), "10")
assert_equal(decimal_to_hexadecimal(255), "FF")
assert_equal(is_valid_number("FF", 16), True)
assert_equal(is_valid_number("G5", 16), False)
assert_equal(is_valid_number("102", 2), False)

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
assert_has(index(State("", 10, "", 0, [], 25)), Button("Open Converter", "converter"))
assert_has(home(State("", 10, "", 0, [], 25)), Button("Learn Conversions", "learn"))
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

