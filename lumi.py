import time, sys, random, string, os, turtle
V = {}
def ap(t):
    for c in t: sys.stdout.write(c); sys.stdout.flush(); time.sleep(0.04)
    print()
def dl():
    try: w = os.get_terminal_size().columns
    except OSError: w = 60
    print("-" * w)
def rp(t):
    cl = ["\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m"]
    print("".join(f"{random.choice(cl)}{c}" for c in t) + "\033[0m")
def sc(n):
    cl = {"red": "31", "green": "32", "yellow": "33", "blue": "34", "purple": "35", "cyan": "36", "white": "37", "reset": "0"}
    sys.stdout.write(f"\033[{cl.get(n.lower(), '37')}m"); sys.stdout.flush()
def rv(t):
    for k, v in V.items(): t = t.replace(f"${k}", str(v))
    return t
def ec(s):
    s = rv(s).strip()
    for op, fn in [("==", lambda a, b: a == b), ("!=", lambda a, b: a != b)]:
        if op in s: l, r = s.split(op, 1); return fn(l.strip().strip('"\''), r.strip().strip('"\''))
    return False
def ht(a):
    if a == "readyWindow": turtle.setup(600, 600); turtle.title("Haiku Turtle"); turtle.bgcolor("black"); turtle.pencolor("white"); turtle.shape("turtle"); turtle.speed(3); turtle.listen()
    elif a == "controlWASD":
        turtle.onkey(lambda: turtle.setheading(90) or turtle.forward(20), "w")
        turtle.onkey(lambda: turtle.setheading(180) or turtle.forward(20), "a")
        turtle.onkey(lambda: turtle.setheading(270) or turtle.forward(20), "s")
        turtle.onkey(lambda: turtle.setheading(0) or turtle.forward(20), "d")
    elif a == "circle": turtle.circle(50)
    elif a == "clear": turtle.clear()
def xl(l):
    global V
    l = l.strip()
    if not l or l.startswith("#"): return "continue"
    if l.startswith("ware "):
        p = l[5:].split("=", 1)
        if len(p) == 2:
            k, v = p[0].strip(), p[1].strip().strip('"\'')
            if v.startswith("random(") and v.endswith(")"):
                ar = v[7:-1].split(",")
                if len(ar) == 2: V[k] = str(random.randint(int(ar[0]), int(ar[1])))
            else: V[k] = v
        return "continue"
    if l == "line()": dl(); return "continue"
    if l == "genpas()":
        ch = string.ascii_letters + string.digits + "!@#$%^&*()"
        print(f"[Сгенерированный пароль]: {''.join(random.choice(ch) for _ in range(16))}"); return "continue"
    if l == "cls()": os.system("clear" if os.name != "nt" else "cls"); return "continue"
    if l == "stop": return "stop"
    if "(" in l and l.endswith(")"):
        fn, ar = l.split("(", 1)[0].strip(), l[l.find("(")+1:-1].strip().strip('"\'')
        if fn == "turtle": ht(ar); return "continue"
        if fn == "turtleSkin": turtle.shape(ar); return "continue"
        if fn == "turtleColor": turtle.color(ar); return "continue"
        ar = rv(ar)
        if fn == "print": print(ar)
        elif fn == "animPrint": ap(ar)
        elif fn == "rainbow": rp(ar)
        elif fn == "color": sc(ar)
        elif fn == "sleep": time.sleep(float(ar))
        elif fn == "input": return input(ar)
        elif fn == "sys": os.system(ar)
    else: print(f"Haiku Error: {l}")
    return "continue"
def pb(bl):
    i, ske = 0, False
    while i < len(bl):
        l = bl[i].strip()
        if not l or l == "loop": i += 1; continue
        if l.startswith("if ") and l.endswith(":"):
            ske = ec(l[3:-1]); i += 1
            while i < len(bl) and (bl[i].startswith(" ") or bl[i].startswith("\t")):
                if ske and xl(bl[i]) == "stop": return "stop"
                i += 1
            continue
        if l.startswith("elif ") and l.endswith(":"):
            cond = ec(l[5:-1]); i += 1
            if not ske and cond:
                ske = True
                while i < len(bl) and (bl[i].startswith(" ") or bl[i].startswith("\t")):
                    if xl(bl[i]) == "stop": return "stop"
                    i += 1
            else:
                while i < len(bl) and (bl[i].startswith(" ") or bl[i].startswith("\t")): i += 1
            continue
        if l == "else:":
            i += 1
            if not ske:
                while i < len(bl) and (bl[i].startswith(" ") or bl[i].startswith("\t")):
                    if xl(bl[i]) == "stop": return "stop"
                    i += 1
            else:
                while i < len(bl) and (bl[i].startswith(" ") or bl[i].startswith("\t")): i += 1
            continue
        if xl(l) == "stop": return "stop"
        i += 1
    return "continue"
def run(f):
    if not os.path.exists(f): print(f"Файл {f} не найден!"); return
    with open(f, "r", encoding="utf-8") as file: lines = file.readlines()
    if any(l.strip() == "loop" for l in lines):
        try:
            while True:
                if pb(lines) == "stop": return
        except KeyboardInterrupt: print("\nПрервано.")
    else:
        try: pb(lines)
        except KeyboardInterrupt: print("\nПрервано.")
    if turtle.Turtle._screen and turtle.getshapes():
        try: turtle.done()
        except: pass
    sc("reset")
def build(f):
    if not os.path.exists(f): print(f"Файл {f} не найден!"); return
    bd = "haiku-builds"
    if not os.path.exists(bd): os.makedirs(bd)
    out_n = os.path.join(bd, os.path.basename(f).rsplit(".", 1)[0] + ".py")
    with open(f, "r", encoding="utf-8") as file: lines = file.readlines()
    with open(out_name := out_n, "w", encoding="utf-8") as out:
        out.write("import time, sys, random, string, os, turtle\nV = {}\n")
        out.write("def ap(t):\n    for c in t: sys.stdout.write(c); sys.stdout.flush(); time.sleep(0.04)\n    print()\n")
        out.write("def dl():\n    try: w = os.get_terminal_size().columns\n    except: w = 60\n    print('-' * w)\n")
        out.write("def rp(t):\n    cl = ['\\033[31m', '\\033[32m', '\\033[33m', '\\033[34m', '\\033[35m', '\\033[36m']\n    print(''.join(f'{random.choice(cl)}{c}' for c in t) + '\\033[0m')\n")
        out.write("def sc(n):\n    cl = {'red': '31', 'green': '32', 'yellow': '33', 'blue': '34', 'purple': '35', 'cyan': '36', 'white': '37', 'reset': '0'}\n    sys.stdout.write(f'\\033[{{cl.get(n.lower(), \"37\")}}m'); sys.stdout.flush()\n")
        out.write("def rv(t):\n    for k, v in V.items(): t = t.replace(f'${{k}}', str(v))\n    return t\n")
        out.write("def ht(a):\n    if a == 'readyWindow': turtle.setup(600, 600); turtle.bgcolor('black'); turtle.pencolor('white'); turtle.shape('turtle'); turtle.speed(3); turtle.listen()\n    elif a == 'controlWASD':\n        turtle.onkey(lambda: turtle.setheading(90) or turtle.forward(20), 'w')\n        turtle.onkey(lambda: turtle.setheading(180) or turtle.forward(20), 'a')\n        turtle.onkey(lambda: turtle.setheading(270) or turtle.forward(20), 's')\n        turtle.onkey(lambda: turtle.setheading(0) or turtle.forward(20), 'd')\n    elif a == 'circle': turtle.circle(50)\n    elif a == 'clear': turtle.clear()\n")
        hl = any(line.strip() == "loop" for line in lines)
        if hl: out.write("try:\n    while True:\n")
        for line in lines:
            l = line.strip()
            if not l or l.startswith("#") or l == "loop": continue
            ind = "        " if hl else "    "
            if line.startswith(" ") or line.startswith("\t"): ind += "    "
            if l.startswith("ware "):
                p = l[5:].split("=", 1)
                k, v = p[0].strip(), p[1].strip()
                if "random(" in v:
                    ar = v[v.find("(")+1:-1].split(",")
                    out.write(f"{ind}V['{k}'] = str(random.randint({ar[0].strip()}, {ar[1].strip()}))\n")
                else: out.write(f"{ind}V['{k}'] = {v}\n")
            elif l.startswith("if ") and l.endswith(":"):
                c = l[3:-1]
                for op in ["==", "!="]:
                    if op in c: left, right = c.split(op, 1); out.write(f"{ind}if rv(f{left.strip()}) {op} rv(f{right.strip()}):\n")
            elif l.startswith("elif ") and l.endswith(":"):
                c = l[5:-1]
                for op in ["==", "!="]:
                    if op in c: left, right = c.split(op, 1); out.write(f"{ind}elif rv(f{left.strip()}) {op} rv(f{right.strip()}):\n")
            elif l == "else:": out.write(f"{ind}else:\n")
            elif l == "line()": out.write(f"{ind}dl()\n")
            elif l == "genpas()": out.write(f"{ind}ch = string.ascii_letters + string.digits + '!@#$%^&*()'; print(f'[Сгенерированный пароль]: ' + ''.join(random.choice(ch) for _ in range(16)))\n")
            elif l == "cls()": out.write(f"{ind}os.system('clear' if os.name != 'nt' else 'cls')\n")
            elif l == "stop": out.write(f"{ind}sys.exit()\n")
            elif "(" in l and l.endswith(")"):
                fn, ar = l.split("(", 1)[0].strip(), l[l.find("(")+1:-1].strip()
                if fn == "turtle": out.write(f"{ind}ht({ar})\n")
                elif fn == "turtleSkin": out.write(f"{ind}turtle.shape({ar})\n")
                elif fn == "turtleColor": out.write(f"{ind}turtle.color({ar})\n")
                elif fn in ["print", "animPrint", "rainbow", "color", "sleep", "input", "sys"]:
                    f_map = {"print": "print(rv(f{ar}))", "animPrint": "ap(rv(f{ar}))", "rainbow": "rp(rv(f{ar}))", "color": "sc(rv(f{ar}))", "sleep": "time.sleep(float(rv(f{ar})))", "input": "input(rv(f{ar}))", "sys": "os.system(rv(f{ar}))"}
                    out.write(f"{ind}{f_map[fn].format(ar=ar)}\n")
        if hl: out.write("except KeyboardInterrupt:\n    print('\\nПрервано.')\n")
        out.write("if turtle.Turtle._screen: turtle.done()\n")
    print("Код скомпилирован!")
if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] in ["run", "build"]: globals()[sys.argv[1]](sys.argv[2])
    else: print("Использование: haiku run/build файл.haiku")
