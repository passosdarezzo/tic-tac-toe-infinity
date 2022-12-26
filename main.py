import pygame
from pygame.locals import MOUSEBUTTONDOWN, Rect, QUIT
from sys import exit
from collections import Counter

# ========================================
# Variables
# ========================================
pontos1, pontos2 = 0, 0
FIM_JOGO = False
VEZ_JOGADOR1 = True
peca = ''
jogadas = dict({
  "00": "", "01": "", "02": "",
  "10": "", "11": "", "12": "",
  "20": "", "21": "", "22": ""
})
clickable_area = [
  [Rect((0, 0), (200, 200)) , Rect((200, 0), (200, 200)), Rect((400, 0), (200, 200))],
  [Rect((0, 200), (200, 200)), Rect((200, 200), (200, 200)), Rect((400, 200), (200, 200))],
  [Rect((0, 400), (200, 200)), Rect((200, 400), (200, 200)), Rect((400, 400), (200, 200))] 
]
position_translation = dict({
  "00": [100, 100], "01": [300, 100], "02": [500, 100],
  "10": [100, 300], "11": [300, 300], "12": [500, 300],
  "20": [100, 500], "21": [300, 500], "22": [500, 500]
}) 

# ========================================
# Methods
# ========================================
def desenha_tabuleiro(tela):
    pygame.draw.line(tela, (255, 255, 255), (200, 0), (200, 600), 10)
    pygame.draw.line(tela, (255, 255, 255), (400, 0), (400, 600), 10)
    pygame.draw.line(tela, (255, 255, 255), (0, 200), (600, 200), 10)
    pygame.draw.line(tela, (255, 255, 255), (0, 400), (600, 400), 10)

def desenha_peca(peca, pos, tela):
  x, y = pos
  img = pygame.image.load(peca + '.png').convert_alpha()
  imgR = pygame.transform.scale(img, (100, 100))
  tela.blit(imgR, (x - 50, y - 50))

def get_casa_clicada(mouse_pos):
  for i in range(len(clickable_area)):
    for j in range(len(clickable_area[i])):
      if clickable_area[i][j].collidepoint(mouse_pos):
        return str(i) + str(j)

def verifica_fim_jogo(peca):
  result = (
    (jogadas["00"] == jogadas["01"] == jogadas["02"] == peca) or
    (jogadas["10"] == jogadas["11"] == jogadas["12"] == peca) or
    (jogadas["20"] == jogadas["21"] == jogadas["22"] == peca) or
    (jogadas["00"] == jogadas["10"] == jogadas["20"] == peca) or
    (jogadas["01"] == jogadas["11"] == jogadas["21"] == peca) or
    (jogadas["02"] == jogadas["12"] == jogadas["22"] == peca) or
    (jogadas["00"] == jogadas["11"] == jogadas["22"] == peca) or
    (jogadas["20"] == jogadas["11"] == jogadas["02"] == peca)
  )
  print(result)
  return result

def texto_vitoria(jogador, tela):
  arial = pygame.font.SysFont('arial', 70)
  mensagem = 'JOGADOR {} VENCEU'.format(jogador)
  mens_vitoria = arial.render(mensagem, True, (0, 255, 0))
  tela.blit(mens_vitoria, (0, 265))

def reset():
  global FIM_JOGO, VEZ_JOGADOR1, jogadas
  VEZ_JOGADOR1 = True
  FIM_JOGO = False
  jogadas = dict({
    "00": "", "01": "", "02": "",
    "10": "", "11": "", "12": "",
    "20": "", "21": "", "22": ""
  })

def desenha_pontos(pontos1, pontos2):
  arial = pygame.font.SysFont('mingliuextbpmingliuextbmingliuhkscsextb', 30)
  jogador1 = 'Jogador1 = {}'.format(pontos1)
  jogador2 = 'Jogador2 = {}'.format(pontos2)

  jd1 = arial.render(jogador1, True, (188, 186, 186))
  jd2 = arial.render(jogador2, True, (188, 186, 186))
  tela.blit(jd1, (0, 0))
  tela.blit(jd2, (420, 0))

def desenha_jogadas(tela):
  for i in jogadas:
    "".__ne__(jogadas[i]) and desenha_peca(jogadas[i], position_translation[i], tela)

def realiza_jogada(casa):
  global VEZ_JOGADOR1
  peca = "x" if VEZ_JOGADOR1 else "o"

  if jogadas[casa] == peca and Counter(jogadas.values())[peca] >= 3 :
    jogadas[casa] = ""
  elif "".__eq__(jogadas[casa]) and Counter(jogadas.values())[peca] < 3:
    jogadas[casa] = peca
    VEZ_JOGADOR1 = not VEZ_JOGADOR1

# ========================================
# Inicialização
# ========================================
pygame.init()
tela = pygame.display.set_mode((600, 600), 0, 32)
pygame.display.set_caption('Jogo da velha')
print(pygame.font.get_fonts())
clock = pygame.time.Clock()

# ========================================
# Main Game loop
# ========================================
while True:
  if not FIM_JOGO:
    # handle Events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        casa = get_casa_clicada(mouse_pos)
        peca = "x" if VEZ_JOGADOR1 else "o"
        print("Voce clicou na casa: " + str(casa))
        realiza_jogada(casa)
        
        FIM_JOGO = verifica_fim_jogo(peca)

    # clear display
    tela.fill((0, 0, 0))

    # draw game objects
    desenha_pontos(pontos1, pontos2)
    desenha_tabuleiro(tela)
    desenha_jogadas(tela)
    if FIM_JOGO:
      texto_vitoria(peca, tela)
      if "x".__eq__(peca):
        pontos1 += 1
      else:
        pontos2 += 1

    # update display
    pygame.display.flip()

    # limit frames per second
    clock.tick(60)
  else:
    for u in pygame.event.get():
      if u.type == QUIT:
          pygame.quit()
          exit()
      if u.type == MOUSEBUTTONDOWN:
          reset()
          #tela.fill(0)

