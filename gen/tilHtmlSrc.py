tilListSrc = """
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
            <a href="../">#Writing</a>
            <a href="/til" class="current-link">#TIL</a>
        </nav>
        <ol id="til-list">
        </ol>
    </section>
</body>

</html>
"""
tilRowSrc = """
<li class="til-row">
    <a href="">
        <h2></h2>
    </a>
</li>
"""
tilPostSrc = """
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
        <div id="post-header">
        <h2></h2>
        <h3></h3>
        </div>
            <div id="post-content"></div>
    </section>
</body>

</html>
"""
