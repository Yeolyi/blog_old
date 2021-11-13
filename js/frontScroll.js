class ScrollBlock {
    constructor(startH, fadingH, endH, appearAnim, disappearAnim) {
        this.startH = startH;
        this.fadingH = fadingH;
        this.endH = endH;
        this.animation = function (height, target) {
            let ret;
            if (height <= fadingH) {
                ret = appearAnim(height, target);
            } else {
                ret = disappearAnim(height, target);
            }

            function defaultMove(height) {
                return easeInOut(startH, endH, height, 0, 0.5);
            }
            if (ret.hasOwnProperty("padding-bottom")) {
                ret["padding-bottom"] += defaultMove(height)
            } else {
                ret["padding-bottom"] = defaultMove(height)
            }
            for (let key in ret) {
                if (key == "padding-bottom") {
                    ret[key] += "em";
                }
            }
            target.css(ret)
        }
    }
}

function easeInOut(startH, endH, curH, startVal, endVal) {
    const p = Math.min(1, (curH - startH) / (endH - startH))

    function easeInOutQuart(x) {
        return x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2;
    }
    return startVal + (endVal - startVal) * easeInOutQuart(p)
}

const scrollBlockOne = new ScrollBlock(0, 700, 1000,
    function (height, target) {
        popPadding = easeInOut(0, 400, height, 0, 2.2)
        newOpacity = easeInOut(0, 600, height, 0.3, 1)
        return {
            "padding-top": "1.25em",
            "padding-bottom": popPadding,
            "opacity": newOpacity
        }
    },
    function (height, target) {
        popPadding = easeInOut(0, 200, 200, 0, 2.2)
        newOpacity = easeInOut(700, 1000, height, 1, 0)
        return {
            "padding-top": "1.25em",
            "padding-bottom": popPadding,
            "opacity": newOpacity
        }
    }
)

const scrollBlockTwo = new ScrollBlock(0, 700, 1000,
    function (height, target) {
        newOpacity = easeInOut(100, 600, height, 0, 1)
        return {
            "padding-top": "1.25em",
            "opacity": newOpacity
        }
    },
    function (height, target) {
        newOpacity = easeInOut(700, 1000, height, 1, 0)
        return {
            "padding-top": "1.25em",
            "opacity": newOpacity
        }
    }
)

const scrollBlocks = [scrollBlockOne, scrollBlockTwo]

function update() {
    let height = Math.max(0, document.documentElement.scrollTop);
    console.log(height)
    for (let i = 0; i < scrollBlocks.length; i++) {
        const element = scrollBlocks[i];
        if (element.startH <= height && height <= element.endH) {
            target = $(".big-text:nth-child(" + (i + 1) + ")")
            target.css({
                "display": "inline-block"
            })
            element.animation(height, $(".big-text:nth-child(" + (i + 1) + ")"))
        } else {
            $(".big-text:nth-child(" + (i + 1) + ")").css({
                "display": "none"
            })
        }
    }
}

$(update)
document.addEventListener('scroll', function () {
    update()
});