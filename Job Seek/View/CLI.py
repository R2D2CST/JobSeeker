"""

Job Seeker

Created by: R2D2CST

Created: 24/sep/2026

"""

# Python Modules.
import unittest
from unittest.mock import patch

# Third Party Libraries.
from colorama import init

# Self Built Modules.
from ModelView.ModelView import ModelView

from View.AppStyle import (
    SUCCESS,
    ERROR,
    WARNING,
    PROMPT,
    BANNER,
    HEADER_STYLE,
    SUB_HEADER_STYLE,
    BOLD_TEXT,
    TEXT,
    MUTED_TEXT,
    STYLE_RESET,
)


class CommandLineInterface:

    def __init__(self):
        """
        Starts the main elements required for this class in order to work.
        Args:
            None
        Returns:
            None
        Raises:
            None
        """
        # Starts colorama color and style modifier.
        init()

        # Valid yes / no (bool) answers in lower case for normalization
        self.validYes: list[str] = ["yes", "y", "si", "s"]
        self.validNo: list[str] = ["no", "n"]
        self.validTrue: list[str] = ["true", "t", "1"]
        self.validFalse: list[str] = ["false", "f", "0"]

        # Initializes model view object.
        self.modelView = ModelView()

        # Main menu options.
        self.mainMenuOptions: list[str] = [
            "Exit.",
            "Modify user keys.",
        ]

        pass

    def start(self) -> None:
        """
        Start entry point into the application.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """

        self._mainLoop()

        pass

    def _applicationHeader(self):
        "Starts the application header."
        print(f"{BANNER}{60*"="}{STYLE_RESET}")
        print(
            f"{BANNER}|{17*" "}{self.modelView.APP_NAME} Version:{self.modelView.APP_VERSION}{17*" "}|{STYLE_RESET}"
        )
        print(f"{BANNER}{60*"="}{STYLE_RESET}")
        pass

    # * Interface loop methods.

    def _mainLoop(self):
        while True:

            self._applicationHeader()

            # Input request.
            for number, option in enumerate(self.mainMenuOptions):
                print(f"{BOLD_TEXT}{number}.- {TEXT}{option}")
            response = self._integerInput()

            # * Exit Application Selection
            if response == 0:  # Exit.
                break
            continue
        pass

    # * User input methods.

    def _stringInput(
        self, promptMessage: str = "Enter text: ", allowEmpty: bool = False
    ) -> str:
        """
        Captures a string input from the user.

        Args:
            promptMessage (str): Message shown to the user in bold.
            allowEmpty (bool): If False, raises ValueError on empty or whitespace strings.

        Returns:
            str: Validated non-empty string.

        Raises:
            ValueError: If input is empty when allowEmpty is False.
        """
        while True:
            try:
                userInput: str = input(
                    f"{BOLD_TEXT}{promptMessage}{STYLE_RESET}"
                ).strip()
                if not allowEmpty and not userInput:
                    raise ValueError("Input cannot be empty or contain only spaces.")
                return userInput
            except ValueError as errorException:
                print(f"{ERROR}Error:{errorException}{STYLE_RESET}")
        # While finish
        pass

    def _integerInput(self, promptMessage: str = "Enter an integer number: ") -> int:
        """
        Captures an integer input from the user.

        Args:
            promptMessage (str): Message shown to the user in bold.

        Returns:
            int: Converted integer value.

        Raises:
            ValueError: If input cannot be converted to integer.
        """
        while True:
            try:
                rawInput: str = input(
                    f"{BOLD_TEXT}{promptMessage}{STYLE_RESET}"
                ).strip()
                if not rawInput:
                    raise ValueError("Value cannot be empty.")
                numberInput: int = int(rawInput)
                return numberInput
            except ValueError as errorException:
                print(
                    f"{ERROR}Invalid option: Please type a valid round number e.g. 0, 1, 2... ({errorException}){STYLE_RESET}"
                )
        # While finish
        pass

    def _boolInput(self, promptMessage: str = "Enter boolean (True/False): ") -> bool:
        """
        Captures a boolean representation from the user.

        Args:
            promptMessage (str): Message shown to the user in bold.

        Returns:
            bool: Parsed boolean result.

        Raises:
            TypeError: If input string does not match valid boolean constants.
        """
        while True:
            try:
                rawInput: str = (
                    input(f"{BOLD_TEXT}{promptMessage}{STYLE_RESET}").strip().lower()
                )
                if rawInput in self.validTrue:
                    return True
                elif rawInput in self.validFalse:
                    return False
                else:
                    raise TypeError(
                        f"'{rawInput}' is not a valid boolean value. Use True/False, T/F, or 1/0."
                    )
            except TypeError as errorException:
                print(f"{ERROR}Type Error: {errorException}{STYLE_RESET}")
        # While finish
        pass

    def _yesNoInput(self, promptMessage: str = "Proceed? (Yes/No): ") -> bool:
        """
        Captures a Yes/No confirmation from the user.

        Args:
            promptMessage (str): Message shown to the user in bold.

        Returns:
            bool: True if input is affirmative, False if negative.

        Raises:
            ValueError: If input does not match expected options.
        """
        while True:
            try:
                rawInput: str = (
                    input(f"{BOLD_TEXT}{promptMessage}{STYLE_RESET}").strip().lower()
                )
                if rawInput in self.validYes:
                    return True
                elif rawInput in self.validNo:
                    return False
                else:
                    raise ValueError(
                        f"'{rawInput}' is not recognized. Options: {self.validYes + self.validNo}"
                    )
            except ValueError as errorException:
                print(f"{ERROR}Invalid Input: {errorException}{STYLE_RESET}")
        # While finish
        pass

    pass


class TestCommandLineInterface(unittest.TestCase):
    """
    Test suite for CommandLineInterface user input capture and control flow methods.

    EXPLICACIÓN PARA PRINCIPIANTES:
    Heredar de 'unittest.TestCase' transforma esta clase en un laboratorio de pruebas automatizadas.
    Cada método que empiece con la palabra 'test' será ejecutado automáticamente por el framework.
    """

    def setUp(self) -> None:
        """
        Executes automatically BEFORE EVERY SINGLE TEST METHOD.

        EXPLICACIÓN PARA PRINCIPIANTES:
        En lugar de crear una instancia de la CLI manualmente dentro de cada prueba,
        'setUp' se encarga de crear un objeto limpio e independiente (self.cliInstance)
        antes de que inicie cada prueba. Esto evita la contaminación de datos entre tests.
        """
        self.cliInstance: CommandLineInterface = CommandLineInterface()

    def testStringInputSuccess(self) -> None:
        """
        Tests _stringInput with a valid string entry on the first try.

        EXPLICACIÓN PARA PRINCIPIANTES:
        - 'expectedValue': Define el resultado que ESPERAMOS obtener.
        - 'patch("builtins.input", return_value="Developer")': Simula que el usuario escribió
          "Developer" y presionó Enter en la consola.
        - 'self.assertEqual': Compara el resultado real devuelto por la función contra el valor esperado.
          Si no son exactamente iguales, la prueba Falla (Fail).
        """
        expectedValue: str = "Developer"

        # Interceptamos la función input() del teclado y devolvemos "Developer"
        with patch("builtins.input", return_value="Developer"):
            resultValue: str = self.cliInstance._stringInput(
                promptMessage="Enter job title: "
            )
            # Verificación de calidad: ¿El método retornó lo mismo que el usuario escribió?
            self.assertEqual(resultValue, expectedValue)

    def testStringInputRecoveryAfterEmpty(self) -> None:
        """
        Tests _stringInput error handling when empty strings are provided first,
        followed by a valid string.

        EXPLICACIÓN PARA PRINCIPIANTES:
        - 'side_effect=["", "   ", "Valid String"]': Simula una racha de intentos del usuario.
          1. Primer intento: Presiona Enter sin escribir nada ("").
          2. Segundo intento: Escribe solo espacios en blanco ("   ").
          3. Tercer intento: Escribe un texto válido ("Valid String").
        - Esta prueba demuestra que el programa NO se rompe ni acepta texto vacío cuando
          'allowEmpty=False', sino que insiste en el bucle 'while' hasta recibir algo válido.
        """
        expectedValue: str = "Valid String"

        with patch("builtins.input", side_effect=["", "   ", "Valid String"]):
            resultValue: str = self.cliInstance._stringInput(
                promptMessage="Enter name: ", allowEmpty=False
            )
            # Verificación: Tras los dos errores iniciales, debe retornar el valor válido del 3er intento.
            self.assertEqual(resultValue, expectedValue)

    def testIntegerInputSuccess(self) -> None:
        """
        Tests _integerInput with valid numerical inputs.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Verifica que el texto "42" (string) ingresado en la consola sea convertido
        correctamente al tipo de dato numérico 42 (int).
        """
        expectedValue: int = 42

        with patch("builtins.input", return_value="42"):
            resultValue: int = self.cliInstance._integerInput(
                promptMessage="Enter age: "
            )
            self.assertEqual(resultValue, expectedValue)

    def testIntegerInputRecoveryAfterInvalid(self) -> None:
        """
        Tests _integerInput error handling when invalid types/letters are passed first.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Simula que el usuario comete errores al ingresar números:
        1. Escribe texto no numérico ("invalid_text") -> Captura ValueError.
        2. Escribe un número decimal ("12.5") -> Captura ValueError (se espera entero).
        3. Escribe un número entero válido ("10") -> Éxito.
        La prueba verifica que el método se recupere correctamente de múltiples errores.
        """
        expectedValue: int = 10

        with patch("builtins.input", side_effect=["invalid_text", "12.5", "10"]):
            resultValue: int = self.cliInstance._integerInput(
                promptMessage="Select option: "
            )
            self.assertEqual(resultValue, expectedValue)

    def testBoolInputTrueAndFalse(self) -> None:
        """
        Tests _boolInput with valid true/false entries.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Evalúa que diferentes variaciones válidas de booleanos se interpreten correctamente:
        - "true" debe convertirse en True booleano.
        - "0" debe convertirse en False booleano.
        Utiliza 'assertTrue' y 'assertFalse' para validar la lógica binaria.
        """
        with patch("builtins.input", side_effect=["true", "0"]):
            trueResult: bool = self.cliInstance._boolInput(
                promptMessage="Enable logs: "
            )
            falseResult: bool = self.cliInstance._boolInput(
                promptMessage="Enable debug: "
            )
            # Verificaciones booleanas explícitas
            self.assertTrue(trueResult)
            self.assertFalse(falseResult)

    def testBoolInputRecoveryAfterTypeError(self) -> None:
        """
        Tests _boolInput error handling when passing invalid text before a valid boolean string.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Simula que el usuario escribe respuestas ambiguas como "not_a_bool" o "maybe"
        que lanzan un TypeError, y luego corrige escribiendo "T".
        Demuestra la tolerancia a fallos del método.
        """
        with patch("builtins.input", side_effect=["not_a_bool", "maybe", "T"]):
            resultValue: bool = self.cliInstance._boolInput(promptMessage="Confirm: ")
            self.assertTrue(resultValue)

    def testYesNoInputPositiveAndNegative(self) -> None:
        """
        Tests _yesNoInput with valid affirmative and negative strings.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Evalúa la captura de confirmaciones en español/inglés:
        - "Si" debe retornar True.
        - "N" debe retornar False.
        """
        with patch("builtins.input", side_effect=["Si", "N"]):
            affirmativeResult: bool = self.cliInstance._yesNoInput(
                promptMessage="Save changes?: "
            )
            negativeResult: bool = self.cliInstance._yesNoInput(
                promptMessage="Delete file?: "
            )
            self.assertTrue(affirmativeResult)
            self.assertFalse(negativeResult)

    def testYesNoInputRecoveryAfterValueError(self) -> None:
        """
        Tests _yesNoInput error recovery when feeding inputs outside validYes/validNo arrays.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Si el usuario ingresa respuestas inválidas como "unknown" o "99", el sistema lanza un ValueError.
        Al tercer intento ingresa "yes", recuperando la ejecución limpia.
        """
        with patch("builtins.input", side_effect=["unknown", "99", "yes"]):
            resultValue: bool = self.cliInstance._yesNoInput(
                promptMessage="Continue?: "
            )
            self.assertTrue(resultValue)

    def testMainLoopExecutionAndExit(self) -> None:
        """
        Tests execution of _MainLoop until exit option (0) is selected.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Prueba el flujo del menú principal.
        Simula que el usuario elige la opción "0" (Exit).
        'try-except' combinado con 'self.fail' garantiza que si el bucle del menú
        lanza una excepción inesperada, la prueba marcará un fallo explícito.
        """
        with patch("builtins.input", return_value="0"):
            try:
                self.cliInstance._MainLoop()
            except Exception as testException:
                self.fail(f"_MainLoop raised an unexpected exception: {testException}")

    def testStartEntryPoint(self) -> None:
        """
        Tests start entry point execution.

        EXPLICACIÓN PARA PRINCIPIANTES:
        Valida que el método público principal 'start()' inicie el flujo de la aplicación
        y finalice de forma limpia al recibir la señal de salida ("0").
        """
        with patch("builtins.input", return_value="0"):
            try:
                self.cliInstance.start()
            except Exception as testException:
                self.fail(
                    f"start method raised an unexpected exception: {testException}"
                )


def runAllCliTests() -> None:
    """
    Executes the unit test suite and formats output logs.

    Main orchestrator function for the unit test suite:
    1. Prints a header styled for the consol.
    2. Loads all the test in class 'TestCommandLineInterface'.
    3. Executes runner with 'verbosity=2' to show a detailed step by step report.
    4. Shows a final message with success or warning depending on the findings.

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    print(f"\n{BANNER}=========================================={STYLE_RESET}")
    print(f"{BANNER} Executing CommandLineInterface Unit Tests {STYLE_RESET}")
    print(f"{BANNER}=========================================={STYLE_RESET}\n")

    # Configuración del ejecutor de pruebas con reporte detallado (verbosity=2)
    testRunner: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)

    # Carga de la suite de pruebas desde la clase
    testSuite: unittest.TestSuite = unittest.TestLoader().loadTestsFromTestCase(
        TestCommandLineInterface
    )

    # Ejecución de la suite y almacenamiento del resultado
    testResult: unittest.TestResult = testRunner.run(testSuite)

    # Evaluación global de calidad
    if testResult.wasSuccessful():
        print(f"\n{SUCCESS}All CLI tests passed successfully!{STYLE_RESET}\n")
    else:
        print(f"\n{WARNING}Some tests failed. Review output log above.{STYLE_RESET}\n")


if __name__ == "__main__":
    # !Allows to execute all the unit test battery tests when code is executed.
    runAllCliTests()
