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
        <nav>
            <a href="" class="current-link">#Writing</a>
            <a href="til">#TIL</a>
        </nav>
    <ol id="post-list">
    </ol>
    <!--
    <div id="post-nav">
      <button id="post-nav-prev">Prev</button>
      <button id="post-nav-next">Next</button>
    </div>
    __>
  </section>
</body>

</html>"""
postRowHtmlSrc = """
<li class="post-row">
        <a href="">
          <h2></h2>
          <h3 class="post-row__date"></h3>
          <h3 class="post-row__tag"> 태그1 태그2 태그3 </h3>
        </a>
      </li>
"""
