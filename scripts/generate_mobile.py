from svg import GRAY, command, save, text

parts=command('ls ./currently-building')
for i,v in enumerate(['Web Products','Interactive Frontends','Personal Experiments']):
    parts+=text(28,91+i*28,f'0{i+1}',14,GRAY)+text(70,91+i*28,v,14)
parts+=text(28,203,'Shipping small things.',14,GRAY)+text(28,231,'Building larger ones.',14,GRAY)
save('building-mobile.svg',440,259,'Currently building Web Products, Interactive Frontends and Personal Experiments.',parts)
parts=command('cat ./toolbox')+text(28,85,'Frontend',14,GRAY)
for y,v in [(113,'React / Next.js'),(141,'TypeScript')]:
    parts+=text(28,y,v,14)
parts+='<path d="M28 183H412" stroke="#252b34"/>'
parts+=text(28,225,'Also working with',14,GRAY)
parts+=text(28,253,'Payload CMS / React Native',14)+text(28,281,'Expo / Flutter / FastAPI',14)
save('tech-mobile.svg',440,319,'Frontend tools and secondary tooling',parts)
save('footer-mobile.svg',440,79,'still building.',text(28,46,'> still building.',14))
