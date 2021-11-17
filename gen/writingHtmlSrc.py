writingPostSrc = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/css/ui.css">
  <title>YeolYi</title>
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
    <div id="post-header">
      <h2></h2>
      <h3></h3>
    </div>
    <div id="post-content"></div>
  </section>
</body>

</html>
"""
writingListSrc = """
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
            <a href="til">#TIL</a>
            <a href="archieve">#Archieve</a>
            <a href="" class="current-link">#Writing</a>
            <div id="nav-explanation">기록할만한 지난 경험들</div>
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
writingRowSrc = """
<li class="post-row">
        <a href="">
          <h2></h2>
          <h3 class="post-row__date"></h3>
          <h3 class="post-row__tag"> 태그1 태그2 태그3 </h3>
        </a>
      </li>
"""
