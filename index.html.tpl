<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="utf-8">
      <meta name="description" content="DiceRV - Dice Random Variables Made
      Easy">
      <meta name="author" content="{{ author }}">
      <meta name="viewport" content="width=device-width">
      <link rel="stylesheet" href="/css/syntax.css">
      <link rel="stylesheet" href="/css/main.css">
      <link rel="stylesheet" href="/css/normalize.css">
      <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
      <link rel="icon" href="/favicon.ico" type="image/x-icon">
      <link rel="alternate" type="application/atom+xml" href="/atom.xml">
      <script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
      <title>{{ title }}</title>
   </head>
   
   <body>
      <main>
         <header>
         <h1 class="title"><a href="{{ baseurl }}">{{ title }}</a></h1>
         </header>

         <div id="home">
             <p class="intro">{{ intro }}
             (<a href="{{ github_url }}">fork</a>).</p>

             <h2>Install</h2>
             <p>TBA.</p>

             <h2>Basic Usage</h2>
             <div class="highlight">
                 <pre><code><span class="kn">import</span> <span class="nn">drv.game.basic</span>
<span class="n">dice</span> <span class="o">=</span> <span class="n">drv</span><span class="o">.</span><span class="n">game</span><span class="o">.</span><span class="n">basic</span><span class="o">.</span><span class="n">ndk</span><span class="p">(</span><span class="mi">3</span><span class="p">,</span> <span class="mi">6</span><span class="p">)</span>
<span class="k">print</span> <span class="n">dice</span><span class="o">.</span><span class="n">mean</span>
</code></pre>
             </div>
             

             <h2>Examples</h2>
             <ul class="posts">

                 <li><span>...</span> <a href="/examples/d20/3d6">3d6</a></li>

             </ul>
             <hr>
             <p>
                 <a href="{{ github_url }}"><img src="/img/cat.png" /></a>
             </p>
         </div>

      </main>


   </body>
</html>
