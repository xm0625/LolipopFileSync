<!doctype html>
     <head>
         <link rel="stylesheet" type="text/css" href="/css/style.css">
         <title>Bottle-MVC</title>
     </head>
     <body>
         <a style="text-align:center" href="/">Home</a>
         <a style="text-align:center" href="http://salimane.com">About</a>
         <div class="page">
             <h1>Bottle MVC Boilerplate</h1>
             % if message is not '':
                 <div class="flash">{{ message }}</div>
             %end
             {{!base}}
        </div>
    </body>
</html>
