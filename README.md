![hacs_badge](https://img.shields.io/badge/hacs-custom-orange.svg) [![BuyMeCoffee][buymecoffeebedge]][buymecoffee]

# Convenia Sensor Component

![logo.jpg](logo.png)

Componente customizado para obter informações sobre suas holerites presentes na [convenia.com.br](https://www.convenia.com.br/) para o home assistant.

# Instalação

## HACS

- Tenha o [HACS](https://hacs.xyz/) instalado, isso permitirá que você atualize facilmente.
- Adicione https://github.com/hudsonbrendon/sensor.convenia como um repositório personalizado do Tipo: Integração
- Clique em Instalar na integração "Convenia".
- Reinicie Home-Assistant.

## Manual

- Copie o diretório custom_components/convenia para o seu diretório <config dir>/custom_components.
- Configure.
- Reinicie o Home-Assistant.

# Configuração

```yaml
- platform: convenia
  employe_name: your-employe-name
  companie_id: your-companie-id
  employe_id: your-employe-id
  token: your-token
```
# Debugando

```yaml
logger:
  default: info
  logs:
    custom_components.convenia: debug
```

[buymecoffee]: https://www.buymeacoffee.com/hudsonbrendon
[buymecoffeebedge]: https://camo.githubusercontent.com/cd005dca0ef55d7725912ec03a936d3a7c8de5b5/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6275792532306d6525323061253230636f666665652d646f6e6174652d79656c6c6f772e737667