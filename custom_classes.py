class Calculator:
    def __init__(self):
        # Starts the calculator at 0
        self._current_val = 0
        
    def add(self, value):
        self._current_val += value 
        return self._current_val

    def sub(self, value):
        self._current_val -= value
        return self._current_val
        
    def multiply(self, value):
        self._current_val *= value
        return self._current_val
        
    def divide(self, value):
        if value == 0:
            raise ValueError("Cannot divide by zero.")
        self._current_val /= value
        return self._current_val

    def clear(self):
        self._current_val = 0
        return self._current_val