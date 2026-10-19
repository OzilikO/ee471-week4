/**
 * Calculator Front-End Logic
 * EE471 Week 4 - Section 1 Part 2
 *
 * All calculations are performed by the Flask backend via POST /api/calculate.
 * No calculations are done locally in JavaScript.
 */

// Calculator state
const calculatorState = {
  displayValue: '0',
  firstOperand: null,
  operator: null,
  waitingForSecondOperand: false,
  isError: false
};

const displayElement = document.getElementById('display');
const keypadElement = document.querySelector('.keypad');

/**
 * Updates the calculator display and adapts typography for long text/errors
 */
function updateDisplay() {
  displayElement.textContent = calculatorState.displayValue;

  displayElement.classList.remove('shrink-text', 'error-text');
  if (calculatorState.isError) {
    displayElement.classList.add('error-text');
  } else if (calculatorState.displayValue.length > 8) {
    displayElement.classList.add('shrink-text');
  }
}

/**
 * Clears/resets the calculator state
 */
function clearCalculator() {
  calculatorState.displayValue = '0';
  calculatorState.firstOperand = null;
  calculatorState.operator = null;
  calculatorState.waitingForSecondOperand = false;
  calculatorState.isError = false;
  updateDisplay();
}

/**
 * Handles numeric digit input (0-9)
 */
function inputDigit(digit) {
  if (calculatorState.isError) {
    clearCalculator();
  }

  const { displayValue, waitingForSecondOperand } = calculatorState;

  if (waitingForSecondOperand) {
    calculatorState.displayValue = digit;
    calculatorState.waitingForSecondOperand = false;
  } else {
    calculatorState.displayValue = displayValue === '0' ? digit : displayValue + digit;
  }
  updateDisplay();
}

/**
 * Handles decimal dot input (.)
 */
function inputDecimal() {
  if (calculatorState.isError) {
    clearCalculator();
  }

  if (calculatorState.waitingForSecondOperand) {
    calculatorState.displayValue = '0.';
    calculatorState.waitingForSecondOperand = false;
    updateDisplay();
    return;
  }

  if (!calculatorState.displayValue.includes('.')) {
    calculatorState.displayValue += '.';
    updateDisplay();
  }
}

/**
 * Sends the two numbers and operator to the Flask backend via POST /api/calculate
 * Strictly delegates all calculations to the server.
 */
async function sendCalculationRequest(num1, operator, num2) {
  const payload = {
    num1: num1,
    num2: num2,
    operator: operator
  };

  const response = await fetch('/api/calculate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  if (!response.ok || data.error) {
    throw new Error(data.error || 'Calculation error');
  }

  return data.result;
}

/**
 * Formats valid result for the display
 */
function formatResult(val) {
  if (typeof val === 'number') {
    // Avoid floating point representation quirks while preserving precision
    const formatted = parseFloat(val.toFixed(10));
    return String(formatted);
  }
  return String(val);
}

/**
 * Handles operator input (+, -, *, /)
 */
async function handleOperator(nextOperator) {
  if (calculatorState.isError) {
    clearCalculator();
  }

  const inputValue = parseFloat(calculatorState.displayValue);

  // If user clicks an operator and then another operator before typing a number, update operator
  if (calculatorState.operator && calculatorState.waitingForSecondOperand) {
    calculatorState.operator = nextOperator;
    return;
  }

  if (calculatorState.firstOperand === null && !isNaN(inputValue)) {
    calculatorState.firstOperand = inputValue;
  } else if (calculatorState.operator) {
    try {
      const result = await sendCalculationRequest(
        calculatorState.firstOperand,
        calculatorState.operator,
        inputValue
      );
      calculatorState.displayValue = formatResult(result);
      calculatorState.firstOperand = typeof result === 'number' ? result : parseFloat(result);
      updateDisplay();
    } catch (err) {
      calculatorState.displayValue = err.message || 'Error';
      calculatorState.isError = true;
      calculatorState.firstOperand = null;
      calculatorState.operator = null;
      calculatorState.waitingForSecondOperand = true;
      updateDisplay();
      return;
    }
  }

  calculatorState.waitingForSecondOperand = true;
  calculatorState.operator = nextOperator;
}

/**
 * Handles equals (=) action by triggering backend calculation
 */
async function handleEquals() {
  if (calculatorState.isError) return;

  if (calculatorState.operator === null || calculatorState.firstOperand === null) {
    return;
  }

  const secondOperand = parseFloat(calculatorState.displayValue);

  try {
    const result = await sendCalculationRequest(
      calculatorState.firstOperand,
      calculatorState.operator,
      secondOperand
    );

    calculatorState.displayValue = formatResult(result);
    calculatorState.firstOperand = null;
    calculatorState.operator = null;
    calculatorState.waitingForSecondOperand = true;
    updateDisplay();
  } catch (err) {
    // Display error message (e.g. "Cannot divide by zero." or "Invalid input...")
    calculatorState.displayValue = err.message || 'Error';
    calculatorState.isError = true;
    calculatorState.firstOperand = null;
    calculatorState.operator = null;
    calculatorState.waitingForSecondOperand = true;
    updateDisplay();
  }
}

/**
 * Keypad button click event listener
 */
keypadElement.addEventListener('click', (event) => {
  const target = event.target.closest('button');
  if (!target) return;

  if (target.dataset.value) {
    if (target.dataset.value === '.') {
      inputDecimal();
    } else {
      inputDigit(target.dataset.value);
    }
  } else if (target.dataset.operator) {
    handleOperator(target.dataset.operator);
  } else if (target.dataset.action === 'equals') {
    handleEquals();
  }
});

/**
 * Clicking the display resets/clears the calculator
 */
displayElement.addEventListener('click', () => {
  clearCalculator();
});

/**
 * Keyboard input support
 */
window.addEventListener('keydown', (event) => {
  const key = event.key;

  if (key >= '0' && key <= '9') {
    inputDigit(key);
  } else if (key === '.') {
    inputDecimal();
  } else if (key === '+' || key === '-') {
    handleOperator(key);
  } else if (key === '*') {
    handleOperator('*');
  } else if (key === '/') {
    event.preventDefault(); // Prevent browser quick search shortcut
    handleOperator('/');
  } else if (key === 'Enter' || key === '=') {
    event.preventDefault();
    handleEquals();
  } else if (key === 'Escape' || key.toLowerCase() === 'c') {
    clearCalculator();
  } else if (key === 'Backspace') {
    if (!calculatorState.waitingForSecondOperand && !calculatorState.isError) {
      if (calculatorState.displayValue.length > 1) {
        calculatorState.displayValue = calculatorState.displayValue.slice(0, -1);
      } else {
        calculatorState.displayValue = '0';
      }
      updateDisplay();
    }
  }
});

// Initial display setup
updateDisplay();
