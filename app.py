from flask import Flask, request, jsonify, render_template
from custom_classes import Calculator  # Import OOP class

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='') 
# Flask bir web sunucusudur. Bu kod parçası sunucuyu başlatır ve index.html gibi dosyaların nerede olduğunu sunucuya öğretir.

@app.route('/') # http: //127.0.0.1:5000 adresine girdiğinde karşılarına çıkan ilk arayüzü gösterir.
def home():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST']) #The endpoint handles all computation requests coming from the frontend
def calculate():
    data = request.get_json()
    
    try:
        num1 = float(data.get('num1'))
        num2 = float(data.get('num2'))
        operator = data.get('operator')
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input. Please provide numbers."}), 400

    calc = Calculator()
    calc.add(num1)  # Set initial value to num1

    try:
        if operator == '+':
            result = calc.add(num2)
        elif operator == '-':
            result = calc.sub(num2)
        elif operator in ['x', '*']:
            result = calc.multiply(num2)
        elif operator in ['÷', '/']:
            result = calc.divide(num2)
        else:
            return jsonify({"error": "Unknown operator."}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000) # web sunucusunu bilgisayarında 5000 numaralı portta aktif olarak çalıştırır