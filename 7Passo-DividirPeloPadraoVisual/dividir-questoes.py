"""
Propósito: Dividir as questões por padrão visual vertical.
Ajustado para: Detectar faixa de ~65px de altura da cor RGB (189, 188, 188).
"""

from PIL import Image
import os

def encontrar_faixa_cinza(imagem, cor_alvo=(189, 188, 188), tolerancia_cor=15, altura_esperada=65, margem_altura=3):
    """
    Encontra posições onde há uma faixa vertical contínua da cor especificada no penúltimo pixel.
    Considera uma margem de erro na altura da faixa.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    altura_minima = altura_esperada - margem_altura  # 62 px
    altura_maxima = altura_esperada + margem_altura  # 68 px
    
    x = largura - 2  # Penúltimo pixel da direita
    y = 0
    
    while y < altura:
        # Verifica se o pixel atual atende à cor alvo
        pixel = pixels[x, y]
        r, g, b = pixel[:3]
        
        if (abs(r - cor_alvo[0]) <= tolerancia_cor and 
            abs(g - cor_alvo[1]) <= tolerancia_cor and 
            abs(b - cor_alvo[2]) <= tolerancia_cor):
            
            # Mede a altura contínua desta cor
            inicio_faixa = y
            comprimento = 0
            
            while y < altura:
                p = pixels[x, y]
                pr, pg, pb = p[:3]
                if (abs(pr - cor_alvo[0]) <= tolerancia_cor and 
                    abs(pg - cor_alvo[1]) <= tolerancia_cor and 
                    abs(pb - cor_alvo[2]) <= tolerancia_cor):
                    comprimento += 1
                    y += 1
                else:
                    break
            
            # Valida se a altura encontrada está dentro da margem de erro (62 a 68 px)
            if altura_minima <= comprimento <= altura_maxima:
                posicoes_corte.append(inicio_faixa)
                print(f"Padrão encontrado em y={inicio_faixa} com altura de {comprimento}px. Cortando em y={inicio_faixa}.")
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo=(189, 188, 188)):
    """
    Divide a imagem verticalmente nas posições onde o padrão foi detectado.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_cinza(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem com os parâmetros fornecidos!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} ocorrências do padrão para corte.")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Salva o bloco final restante da imagem
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Substitua pela sua imagem
    pasta_saida = "resultado_questoes"                       # Nome da pasta final
    
    cor_do_padrao = (189, 188, 188)  # RGB 0-255 fornecido
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    
    print("Processo concluído!")