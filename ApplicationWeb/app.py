from flask import Flask, render_template, request, jsonify
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    model = data.get('model')

    try:
        if model == '1':
            # Chapitre 1 - 2 variables
            c1  = float(data['c1'])
            c2  = float(data['c2'])
            a11 = float(data['a11']); a12 = float(data['a12']); b1 = float(data['b1'])
            a21 = float(data['a21']); a22 = float(data['a22']); b2 = float(data['b2'])
            x1min = float(data['x1min'])

            c = [-c1, -c2]
            A = [[a11, a12], [a21, a22], [-1, 0]]
            b = [b1, b2, -x1min]

            result = linprog(c, A_ub=A, b_ub=b,
                           bounds=[(0, None), (0, None)],
                           method='highs')

            if result.success:
                return jsonify({
                    'success': True,
                    'model': '1',
                    'x1': round(result.x[0], 4),
                    'x2': round(result.x[1], 4),
                    'z':  round(-result.fun, 4)
                })

        elif model == '2':
            # Chapitre 2 - 3 variables
            c1  = float(data['c1'])
            c2  = float(data['c2'])
            c3  = float(data['c3'])
            a11 = float(data['a11']); a12 = float(data['a12']); a13 = float(data['a13']); b1 = float(data['b1'])
            a21 = float(data['a21']); a22 = float(data['a22']); a23 = float(data['a23']); b2 = float(data['b2'])
            x1min = float(data['x1min'])
            x3max = float(data['x3max'])

            c = [-c1, -c2, -c3]
            A = [
                [a11, a12, a13],
                [a21, a22, a23],
                [-1, 0, 0],
                [0, 0, 1]
            ]
            b = [b1, b2, -x1min, x3max]

            result = linprog(c, A_ub=A, b_ub=b,
                           bounds=[(0, None), (0, None), (0, None)],
                           method='highs')

            if result.success:
                return jsonify({
                    'success': True,
                    'model': '2',
                    'x1': round(result.x[0], 4),
                    'x2': round(result.x[1], 4),
                    'x3': round(result.x[2], 4),
                    'z':  round(-result.fun, 4)
                })

        return jsonify({'success': False, 'error': 'Aucune solution trouvee.'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)