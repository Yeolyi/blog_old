---
title: 알면 좋은 Swift 함수/구문들
date: 1970-01-01
---

``` {class="language-swift"}
print(#"""
\    /\
 )  ( ')
(  /  )
 \(__)|
"""#)
```
*탈출문자 포함된 여러줄 문자열 출력하기*

``` {class="language-swift"}
Character("a").asciiValue!
```
*특정 문자의 아스키 값 알기. 근데 여러 문자로 되어있거나 이모티콘같은거면 nil인가?*


``` {class="language-swift"}
String(repeating: "*", count: i)
```
*반복되는 문자열 출력하기.*

``` {class="language-swift"}
while let input = readLine()?.split(separator: " ").map({ Int($0)! }) {
    print(input[0]+input[1])
}
```
*EOF까지 입력 받기.*