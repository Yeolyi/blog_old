postListHtmlSrc = """
<!DOCTYPE html>

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/css/ui.css">
  <title>YeolYi</title>
  <script src="/js/jquery.js"></script>
  <script src="/js/ui.js"></script>
</head>

<body>
  <header>
    <a href="/" id="yeolyi-logo">YeolYi</a>
    <nav>
      <a href="/stories" class="nav__button">Stories</a>
      <a href="/dev" class="nav__button">Dev</a>
      <a href="/about" class="nav__button">About</a>
    </nav>
  </header>
  <section id="container">
    <ol id="post-list">
    </ol>
    <div id="post-nav">
      <button id="post-nav-prev">&#xE000; Prev</button>
      <button id="post-nav-next">Next &#xE001;</button>
    </div>
  </section>
</body>

</html>"""
postRowHtmlSrc = """
<li class="post-row">
        <a href="">
          <h2></h2>
          <div class="post-row__date"></div>
          <div class="post-row__tag"> 태그1 태그2 태그3 </div>
        </a>
      </li>
"""
