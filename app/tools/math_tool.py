import operator
from typing import Union

def evaluate_math_expression(expression: str) -> Union[int, float, str]:
    """
    Safely evaluates a basic arithmetic expression.
    Supports addition, subtraction, multiplication, and division for two numbers.

    Args:
        expression (str): The arithmetic expression (e.g., "42 * 7").

    Returns:
        Union[int, float, str]: The result of the operation (int or float) or an error message (str).
    """
    # Define supported operators and their corresponding functions
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv, # Use truediv for float division
    }

    # Split the expression into parts: number1, operator, number2
    parts = expression.strip().split()

    # Validate the format of the expression
    if len(parts) != 3:
        return "Invalid math expression format. Expected 'number operator number' (e.g., '42 * 7')."

    try:
        # Convert numbers to float to handle both integers and decimals
        num1 = float(parts[0])
        op_char = parts[1]
        num2 = float(parts[2])

        # Get the operation function
        operation = ops.get(op_char)
        if operation is None:
            return f"Unsupported operator: '{op_char}'. Only +, -, *, / are supported."

        # Perform the calculation
        result = operation(num1, num2)

        # Return integer if the result is a whole number, otherwise float
        return int(result) if result == int(result) else result
    except ValueError:
        return "Invalid numbers in expression. Please ensure numbers are valid (e.g., '10', '5.5')."
    except ZeroDivisionError:
        return "Division by zero is not allowed."
    except Exception as e:
        return f"An unexpected error occurred during math evaluation: {e}"