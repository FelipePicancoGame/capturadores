# App do iPhone (Capacitor) — preparado em 14/nov

- `contentInset: "always"`: o jogo fica abaixo da Dynamic Island/notch e acima da barra de baixo (revisão App Store, item 4). Conferir no TestFlight em iPhone com Dynamic Island.
- `appendUserAgent: "CapturadoresApp"`: liga o modo iPhone do jogo (CVNATIVO): sem loja de dinheiro até ligar a compra da Apple (com RESTAURAR COMPRAS), sem botão de fechar o jogo.
- Em Configurações já tem 🔒 Privacidade (política + Apagar meus dados).
- App Store Connect: classificação 9+, privacidade https://felipepicancogame.github.io/capturadores/privacidade.html, contato capturadoresdovale@gmail.com.

## Compras (15/nov, bloco COMPRAS15NOV)
- Plugin cordova-plugin-purchase (StoreKit). IDs no App Store Connect = com.capturadoresdovale.app.<id>:
  cristais100, cristais550, cristais1200, energia, monstrinhoraro, moedas5000, moedas12000, moedas30000, moedas70000, moedas150000, moedas400000 (consumíveis);
  dobro, automatico, semanuncios (não consumíveis); passe30 (assinatura não renovável, 30 dias, 50 💎 por dia).
- Loja mostra o preço da Apple e o botão RESTAURAR COMPRAS. #compras0 desliga.
## Montar o app
- GitHub Actions > app-iphone > Run workflow (precisa dos segredos ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_P8, APPLE_TEAM_ID). Vai pro TestFlight.
