from flask import Flask, request, jsonify, render_template

# Configuring Flask to look in the current folder for your HTML, CSS, and JS
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

@app.route('/')
def home():
    # This serves the web page you vibe-coded in Step 1
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    try:
        num1 = float(data.get('num1'))
        num2 = float(data.get('num2'))
        operator = data.get('operator')
    except (ValueError, TypeError):
        # Returns an error message for invalid input
        return jsonify({"error": "Invalid input. Please provide numbers."}), 400

    # Performing calculations manually to avoid using eval()
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == 'x' or operator == '*':
        result = num1 * num2
    elif operator == '÷' or operator == '/':
        if num2 == 0:
            # Returns an error message for division by zero
            return jsonify({"error": "Cannot divide by zero."}), 400
        result = num1 / num2
    else:
        return jsonify({"error": "Unknown operator."}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    # Runs the server on localhost
    app.run(debug=True, port=5000)
    app.run(debug=True, port=5000)