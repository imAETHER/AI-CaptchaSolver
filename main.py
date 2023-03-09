from flask import Flask, jsonify, request
from solver import checkUrl, solveCaptcha

app = Flask(__name__)

@app.route('/solve', methods = ['GET'])
def solverApi():
  capUrl = request.args.get('captcha')

  if not checkUrl(capUrl):
    print('Invalid Url: ' + capUrl)
    return jsonify({ 'success': False, 'message': 'Invalid captcha URL provided.' })

  data = solveCaptcha(capUrl)
  if data is None:
    return jsonify({ 'success': False, 'message': 'Captcha solve failed!' })

  return jsonify({ 'success': True, 'solve': data })

if __name__ == '__main__':
  app.run(debug = False, use_evalex=False, port=3007)