from svg import BLUE, GRAY, command, reveal, save, text

parts = command("ls ./currently-building")
for i, value in enumerate(["Web Products", "Interactive Frontends", "Personal Experiments"]):
    y = 91+i*28
    parts += reveal(text(28,y,f"0{i+1}",14,GRAY)+text(78,y,value,14), .12*i)
parts += text(28,203,"Shipping small things. Building larger ones.",14,GRAY)
save("building.svg",880,239,"Currently building: Web Products, Interactive Frontends, Personal Experiments. Shipping small things. Building larger ones.",parts)
parts = command("cat ./toolbox") + text(28,85,"Frontend",14,GRAY)
parts += text(28,113,"React / Next.js / TypeScript",14)
parts += '<path d="M28 155H852" stroke="#252b34"/>'
parts += text(28,197,"Also working with",14,GRAY)
parts += text(28,225,"Payload CMS / React Native / Expo",14)
parts += text(28,253,"Flutter / FastAPI",14)
save("tech.svg",880,291,"Frontend: React, Next.js, TypeScript. Also working with Payload CMS, React Native, Expo, Flutter and FastAPI.",parts)
save("footer.svg",880,79,"still building.",text(28,46,">",14,BLUE)+text(52,46,"still building.",14))
