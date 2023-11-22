from flask import Flask

from threading import Thread

from waitress import serve


app = Flask('')

@app.route('/')

def index():
    return '''<!DOCTYPE html>
<html>
	<head>
		<title>Amazon Alexa#0086</title>
		<style>
			body{
          margin: 0;
          padding: 0;
          background: #0c002b;
      }

      a{
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%,-50%);
          color: #1670f0;
          padding: 30px 60px;
          font-size: 30px;
          letter-spacing: 2px;
          text-transform: uppercase;
          box-shadow: 0 20px 50px rgba(0,0,0,.5);
          overflow: hidden;
          text-decoration: none;

      }
      a:before {
          content: '';
          position: absolute;
          top: 2px;
          left: 2px;
          bottom: 2px;
          width: 50%;
          background: rgba(255,255,255,0.05);

      }

      a span:nth-child(1){
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background: linear-gradient(to right, #0c002b, #1779ff);
          animation: animate1 2s linear infinite;
          animation-delay: 1s;
      }
      @keyframes animate1{
          0%{
              transform: translateX(-100%);
          }
          100%{
              transform: translateX(100%);
          }
      }

      a span:nth-child(2){
          position: absolute;
          top: 0;
          right: 0;
          width: 2px;
          height: 100%;
          background: linear-gradient(to bottom, #0c002b, #1779ff);
          animation: animate2 2s linear infinite;
          
      }
      @keyframes animate2{
          0%{
              transform: translateY(-100%);
          }
          100%{
              transform: translateY(100%);
          }
      }

      a span:nth-child(3){
          position: absolute;
          bottom: 0;
          left: 0;
          width: 100%;
          height: 2px;
          background: linear-gradient(to left, #0c002b, #1779ff);
          animation: animate3 2s linear infinite;

      }
      @keyframes animate3{
          0%{
              transform: translateX(100%);
          }
          100%{
              transform: translateX(-100%);
          }
      }
      a span:nth-child(4){
          position: absolute;
          top: 0;
          left: 0;
          width: 2px;
          height: 100%;
          background: linear-gradient(to top, #0c002b, #1779ff);
          animation: animate4 2s linear infinite;
          animation-delay: 1s;

      }
      @keyframes animate4{
          0%{
              transform: translateY(100%);
          }
          100%{
              transform: translateY(-100%);
          }
      }
		</style>
  </head>
  <body>
    <a href="https://discord.com/api/oauth2/authorize?client_id=896060431578329108&permissions=8&scope=bot">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
      Amazon Alexa#0086
  </a>
  </body>
<html>
  '''


def run():
  serve(app, host="0.0.0.0", port=8080)

def keep_alive():  

    t = Thread(target=run)

    t.start()